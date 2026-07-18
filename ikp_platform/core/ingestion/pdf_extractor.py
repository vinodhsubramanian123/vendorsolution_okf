"""
PDF Extractor — Extracts engineering knowledge from vendor PDF documents.

Governs: Blueprint 04 §8 (PDF Source-Specific Expectations),
         Blueprint 04 §7 (Engineering Object Extraction),
         Implementation Checklist item 3

Extracts engineering meaning from headings, tables, specifications, notes,
warnings, footnotes, and captions. Ignores decorative content.
"""

import re
import json
import fitz  # PyMuPDF
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging

from ikp_platform.core.ontology.models import (
    BaseEngineeringObject,
    EngineeringObjectType,
    EngineeringRelationship,
    RelationshipType,
    EngineeringAttribute,
    EvidenceRecord,
    ConfidenceLevel,
    LifecycleStatus,
    Platform,
    Component,
    Rule,
    RuleSeverity,
    Constraint,
    CategoryLimit,
    SKU,
    Workload,
    Source,
    KnowledgeDelta,
    DeltaChange,
    DeltaChangeType,
    SlotMapping,
    PackagingType,
)

from ikp_platform.core.ingestion.table_parser import TableParser

logger = logging.getLogger("ikp.ingestion")


class PDFExtractor:
    """
    Extracts engineering knowledge from vendor QuickSpecs and technical PDFs.

    Blueprint 04 §8: Extract engineering meaning from headings, tables,
    comparison tables, specifications, notes, warnings, footnotes.
    """

    def __init__(self, source: Source):
        self.source = source
        self.extracted_objects: List[BaseEngineeringObject] = []
        self.delta_changes: List[DeltaChange] = []
        
        # Initialize AI and MCP Clients
        from ikp_platform.core.reasoning.llm_client import LLMClient
        from ikp_platform.core.repository.mcp_client import ObsidianMCPClient
        self.llm_client = LLMClient()
        # Derive repository path from project structure instead of hardcoding
        project_root = Path(__file__).parent.parent.parent.parent
        repository_path = str(project_root / "repository")
        self.mcp_client = ObsidianMCPClient(repository_path)

    def extract(self, file_path: str) -> Tuple[List[BaseEngineeringObject], KnowledgeDelta]:
        """
        Main extraction entry point.
        Returns (list of engineering objects, knowledge delta).
        """
        logger.info(f"Extracting from PDF: {file_path}")
        doc = fitz.open(file_path)
        
        # 1. Deterministic Versioning (Blueprint 04)
        if not self.source.version:
            mod_date = doc.metadata.get("modDate")
            if mod_date:
                clean_date = mod_date.strip("D:").replace("'", "")
                self.source.version = f"modDate_{clean_date}"
            else:
                with open(file_path, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()[:12]
                self.source.version = f"sha256_{file_hash}"
            logger.info(f"Computed Deterministic Version: {self.source.version}")

        full_text = ""
        for page in doc:
            full_text += page.get_text() + "\n\n"
        doc.close()

        # Step 0: Unicode Shield (Normalize typography)
        full_text = self._normalize_text(full_text)

        # Step 1: Extract platform identity
        platform = self._extract_platform_identity(full_text)
        if platform:
            self.extracted_objects.append(platform)
            self._extract_topology(full_text, platform)
            self.delta_changes.append(DeltaChange(
                change_type=DeltaChangeType.NEW_OBJECT,
                object_id=platform.id,
                new_value=platform.title,
            ))

        # Step 1.5: Extract Workloads and Customer Requirements
        workloads = self._extract_workloads_and_requirements(full_text, platform)
        self.extracted_objects.extend(workloads)
        for wl in workloads:
            self.delta_changes.append(DeltaChange(
                change_type=DeltaChangeType.NEW_OBJECT,
                object_id=wl.id,
                new_value=wl.title
            ))

        # Step 2: Extract processors
        processors = self._extract_processors(full_text, platform)
        self.extracted_objects.extend(processors)

        # Step 3: Extract memory specifications
        memory_specs = self._extract_memory(full_text, platform)
        self.extracted_objects.extend(memory_specs)

        # Step 4: Extract storage/drive information
        storage = self._extract_storage(full_text, platform)
        self.extracted_objects.extend(storage)

        # Step 5: Extract networking (OCP/NIC)
        networking = self._extract_networking(full_text, platform)
        self.extracted_objects.extend(networking)

        # Step 6: Extract GPU/Accelerators
        gpus = self._extract_gpus(full_text, platform)
        self.extracted_objects.extend(gpus)

        # Step 7: Extract engineering rules and constraints
        rules = self._extract_rules(full_text, platform)
        self.extracted_objects.extend(rules)

        # Step 7.5: Extract tabular SKUs and components using robust pdfplumber parser
        table_parser = TableParser()
        structured_components = table_parser.parse_document(file_path)
        tabular_objects = self._process_structured_components(structured_components, platform)
        self.extracted_objects.extend(tabular_objects)

        # Step 8: Extract power supplies
        psus = self._extract_power(full_text, platform)
        self.extracted_objects.extend(psus)

        # Step 9: Post-processing (synthesize limits based on components)
        self._post_process_limits(platform)

        # Build Knowledge Delta
        delta = KnowledgeDelta(
            source_id=self.source.source_id,
            changes=self.delta_changes,
        )

        logger.info(
            f"Extracted {len(self.extracted_objects)} objects, "
            f"{len(self.delta_changes)} changes"
        )
        return self.extracted_objects, delta

    # -------------------------------------------------------------------
    # Post-Processing
    # -------------------------------------------------------------------

    def _post_process_limits(self, platform: Optional[Platform]):
        """Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)."""
        if not platform:
            return
            
        platform_id = platform.id
        
        # Count explicit enablement kits or primary/secondary slots
        ocp_slots_found = 0
        risers_found = 0
        
        for obj in self.extracted_objects:
            if obj.type == EngineeringObjectType.COMPONENT:
                title_desc = f"{obj.title} {obj.description}".lower()
                if "ocp" in title_desc and ("slot" in title_desc or "enablement" in title_desc):
                    ocp_slots_found += 1
                if "riser" in title_desc and "cage" in title_desc:
                    risers_found += 1
                    
        # Synthesize CategoryLimit if we found evidence of capacity
        if ocp_slots_found > 0:
            limit_id = f"{platform_id}/limits/max-ocp-slots"
            # check if it already exists
            if not any(obj.id == limit_id for obj in self.extracted_objects):
                cl = CategoryLimit(
                    id=limit_id,
                    title="Max OCP Slots",
                    limit_name="Maximum OCP Slots",
                    limit_value=ocp_slots_found,
                    target_category="Networking",
                    target_subcategory="NIC",
                    vendor=platform.vendor,
                    solution_domain=platform.solution_domain,
                    product_family=platform.product_family,
                    generation=platform.generation,
                    platform_id=platform.id,
                    relationships=[EngineeringRelationship(target_id=platform_id, relationship_type=RelationshipType.CONTAINS)]
                )
                self.extracted_objects.append(cl)
                self.delta_changes.append(DeltaChange(
                    change_type=DeltaChangeType.NEW_OBJECT,
                    object_id=cl.id,
                    new_value=ocp_slots_found,
                ))

    # -------------------------------------------------------------------
    # Platform Identity
    # -------------------------------------------------------------------

    def _human_in_the_loop_fallback(self, text: str) -> Platform:
        """
        Fallback when automated title/vendor/domain extraction fails.

        This does not just raise -- it writes the source's raw candidate
        lines to needs_review/<source_id>.json so a human can map the
        platform identity manually, instead of the document silently
        vanishing with nothing but a log line.
        """
        logger.warning("Automated Platform Identity Extraction Failed or Confidence < 80%. Triggering HITL fallback.")

        review_dir = Path("needs_review")
        review_dir.mkdir(exist_ok=True)
        review_path = review_dir / f"{self.source.source_id}.json"
        candidate_lines = [l.strip() for l in text[:1500].split('\n') if l.strip()][:15]
        with open(review_path, "w", encoding="utf-8") as f:
            json.dump({
                "source_id": self.source.source_id,
                "reason": "Could not confidently determine Vendor, Product Family, or Solution Domain.",
                "candidate_first_lines": candidate_lines,
            }, f, indent=2)

        raise ValueError(
            f"HITL_REQUIRED: The pipeline could not confidently determine Vendor, "
            f"Product Family, or Solution Domain for '{self.source.source_id}'. "
            f"Wrote candidate lines to {review_path} for manual mapping."
        )

    def _infer_solution_domain(self, text: str) -> str:
        text = text[:5000].lower()
        compute_score = text.count("processor") + text.count("memory") + text.count("dimm") + text.count("server") + text.count("proliant") * 10 + text.count("compute") * 5
        storage_score = text.count("storage") + text.count("nvme") + text.count("ssd") + text.count("drive") + text.count("alletra") * 10
        networking_score = text.count("switch") + text.count("transceiver") + text.count("port") + text.count("bandwidth") + text.count("aruba") * 10
        
        scores = {"Compute": compute_score, "Storage": storage_score, "Networking": networking_score}
        best_domain = max(scores, key=scores.get)
        if scores[best_domain] < 2:
            return "Unknown"
        return best_domain

    def _extract_platform_identity(self, text: str) -> Optional[Platform]:
        """Extract the main platform identity from the document using generalized heuristics."""
        vendor = "Unknown"
        family = "Unknown"
        model = "Unknown"
        generation = "Unknown"
        title = "Unknown Platform"
        platform_id = "unknown-platform"
        
        first_lines = text[:2000].split('\n')
        title_found = False
        
        joined_lines = []
        current_block = []
        for line in first_lines:
            line = line.strip()
            if line:
                current_block.append(line)
            else:
                if current_block:
                    joined_lines.append(" ".join(current_block))
                    current_block = []
        if current_block:
            joined_lines.append(" ".join(current_block))
        
        # Strategy 1: Direct regex for "Vendor ProductName" pattern within any line
        # This handles cases where the product name is buried in a longer sentence
        vendor_product_pattern = re.compile(
            r'((?:HPE|Dell|Cisco|Lenovo|IBM|Supermicro)\s+'
            r'(?:ProLiant\s+(?:Compute\s+)?|Alletra\s+(?:Storage\s+)?(?:MP\s+)?|PowerEdge\s+|UCS\s+|ThinkSystem\s+)?'
            r'[\w]+(?:\s+[\w]+){0,4}?'
            r'(?:\s+(?:Gen\s*\d+|G\d+|v\d+))?)'
            r'(?=\s+(?:QuickSpecs|provides|is\s+a|features|supports|delivers)|$)',
            re.IGNORECASE
        )
        
        for line in joined_lines:
            match = vendor_product_pattern.search(line)
            if match:
                candidate = match.group(1).strip()
                # Remove trailing noise words that might have been captured
                candidate = re.sub(r'\s+(?:QuickSpecs|provides|is\s+a|features|supports|delivers).*$', '', candidate, flags=re.IGNORECASE).strip()
                if len(candidate) > 5:
                    title = candidate
                    title_found = True
                    
                    vendor_match = re.search(r'\b(HPE|Dell|Cisco|Lenovo|IBM|Supermicro)\b', title, re.IGNORECASE)
                    if vendor_match:
                        vendor = vendor_match.group(1).upper()
                        if vendor == "DELL": vendor = "Dell"
                        if vendor == "CISCO": vendor = "Cisco"
                        if vendor == "LENOVO": vendor = "Lenovo"
                        if vendor == "SUPERMICRO": vendor = "Supermicro"
                    
                    gen_match = re.search(r'\b(Gen\s*\d+|G\d+|v\d+)\b', title, re.IGNORECASE)
                    if not gen_match:
                        # Fallback: scan the first 500 chars for generation if not in title
                        gen_match = re.search(r'\b(Gen\s*\d+|G\d+|v\d+)\b', text[:500], re.IGNORECASE)
                        
                    if gen_match:
                        generation = gen_match.group(1).replace(" ", "")
                    
                    # Strip vendor and generation from title parts to derive family/model
                    parts = [p for p in title.split() if p.upper() != vendor.upper() and not re.match(r'(?i)^(Gen\d+|G\d+|v\d+|Compute)$', p)]
                    if len(parts) >= 1:
                        family = parts[0]
                    if len(parts) >= 2:
                        model = "-".join(parts[1:])
                    else:
                        model = family
                        
                    platform_id = f"{vendor.lower()}-{family.lower()}-{model.lower()}"
                    if generation != "Unknown":
                        platform_id += f"-{generation.lower()}"
                    break
                    
        solution_domain = self._infer_solution_domain(text)
        
        if not title_found or vendor == "Unknown" or solution_domain == "Unknown":
            return self._human_in_the_loop_fallback(text)
            
        desc = self._extract_description(text)
        form_factor = self._extract_form_factor(text)
        chassis_types = self._extract_chassis_types(text)
        
        attrs = []
        if form_factor:
            attrs.append(EngineeringAttribute(name="Form Factor", value=form_factor))
        for ct in chassis_types:
            attrs.append(EngineeringAttribute(name="Chassis Type", value=ct))
            
        capabilities = self._extract_capabilities(text)
        workloads = self._extract_workload_tags(text)
        
        tags = [solution_domain.lower(), vendor.lower()] + workloads
        if family != "Unknown": tags.append(family.lower())

        platform = Platform(
            id=platform_id.replace(" ", ""),
            title=title,
            description=desc,
            vendor=vendor,
            solution_domain=solution_domain,
            product_family=family,
            generation=generation,
            lifecycle_status=LifecycleStatus.ACTIVE,
            attributes=attrs,
            capabilities=capabilities,
            tags=tags,
            evidence=[EvidenceRecord(
                source_id=self.source.source_id,
                confidence=ConfidenceLevel.HIGH,
                description=f"Automated generic extraction",
                original_text_snippet=title,
            )],
        )
        return platform

    # -------------------------------------------------------------------
    # Workload & Requirements Extraction
    # -------------------------------------------------------------------

    def _extract_workloads_and_requirements(self, text: str, platform: Optional[Platform]) -> List[Workload]:
        """Extract high-level Workloads (Customer Intent) and link to Platform."""
        workloads = []
        if not platform: return workloads
        
        # Scan text for key workloads
        workload_keywords = {
            "Virtualization": ["virtualization", "vmware", "hyper-v", "vdi"],
            "AI and Machine Learning": ["ai", "machine learning", "deep learning", "inferencing"],
            "Database": ["database", "sql", "oracle", "sap hana"],
            "Analytics": ["analytics", "big data", "hadoop"],
            "HPC": ["hpc", "high performance computing"],
            "Storage": ["software-defined storage", "sds", "vsan"]
        }
        
        extracted = set()
        text_lower = text.lower()
        
        # Only scan the first 10000 chars to avoid false positives deep in footnotes
        scan_text = text_lower[:10000]
        
        for wl_name, keywords in workload_keywords.items():
            for kw in keywords:
                if kw in scan_text:
                    extracted.add(wl_name)
                    break
                    
        for idx, wl_name in enumerate(extracted):
            wl_id = f"workload-{wl_name.lower().replace(' and ', '-').replace(' ', '-')}"
            wl = Workload(
                id=wl_id,
                title=wl_name,
                description=f"Supports {wl_name} workloads",
                vendor="Agnostic",  # Workloads are vendor agnostic
                solution_domain=platform.solution_domain if platform else "Unknown",
                performance_requirements={"workload_type": wl_name},
                relationships=[
                    EngineeringRelationship(
                        target_id=platform.id,
                        relationship_type=RelationshipType.SUPPORTS
                    )
                ],
                evidence=[EvidenceRecord(
                    source_id=self.source.source_id,
                    confidence=ConfidenceLevel.HIGH,
                    description=f"Extracted workload from platform overview"
                )]
            )
            workloads.append(wl)
            
        logger.info(f"Extracted {len(workloads)} workloads for {platform.id}")
        return workloads

    # -------------------------------------------------------------------
    # Processor Extraction
    # -------------------------------------------------------------------

    def _extract_processors(self, text: str, platform: Optional[Platform]) -> List[Component]:
        """Extract processor specifications from QuickSpecs tables."""
        processors = []
        platform_id = platform.id if platform else "unknown"

        # Find processor table data
        # Pattern: Model  BaseSpeed  Cores  Cache  Power  UPI  DDR5  SGX  Die
        proc_pattern = re.compile(
            r"(6\d{3}[EP]?)\s+"          # Model (e.g., 6710E, 6507P)
            r"(\d+\.?\d*)\s+"             # Base Speed GHz
            r"(\d+)\s+"                    # Cores
            r"(\d+)\s+"                    # L3 Cache MB
            r"(\d+)\s+"                    # Power W
            r"(\d+)\s+"                    # UPI
            r"(\d+)\s+"                    # DDR5 MT/s
            r"(\d+)\s+"                    # SGX
            r"(\w+)"                       # Die
        )

        for match in proc_pattern.finditer(text):
            model = match.group(1)
            base_speed = match.group(2)
            cores = match.group(3)
            cache = match.group(4)
            power = match.group(5)
            upi = match.group(6)
            ddr5 = match.group(7)
            sgx = match.group(8)
            die = match.group(9)

            # Determine core type
            core_type = "E-Core" if model.endswith("E") else "P-Core"

            proc = Component(
                id=f"{platform_id}/processors/xeon-{model.lower()}",
                title=f"Intel Xeon 6 {model}",
                description=f"Intel Xeon 6 {model} - {cores} {core_type}s, {base_speed}GHz, {power}W TDP",
                vendor="Intel",
                solution_domain=platform.solution_domain if platform else "Unknown",
                product_family=platform.product_family if platform else "Xeon 6",
                generation=platform.generation if platform else "Xeon 6",
                platform_id=platform.id if platform else None,
                component_category="CPU",
                lifecycle_status=LifecycleStatus.ACTIVE,
                capabilities=[core_type, "DDR5", f"PCIe Gen5"],
                attributes=[
                    EngineeringAttribute(name="Base Speed", value=float(base_speed), unit="GHz"),
                    EngineeringAttribute(name="Cores", value=int(cores)),
                    EngineeringAttribute(name="L3 Cache", value=int(cache), unit="MB"),
                    EngineeringAttribute(name="TDP", value=int(power), unit="W"),
                    EngineeringAttribute(name="UPI Links", value=int(upi)),
                    EngineeringAttribute(name="DDR5 Speed", value=int(ddr5), unit="MT/s"),
                    EngineeringAttribute(name="SGX Enclave", value=int(sgx), unit="GB"),
                    EngineeringAttribute(name="Die Type", value=die),
                    EngineeringAttribute(name="Core Type", value=core_type),
                ],
                tags=["cpu", "intel", "xeon", core_type.lower().replace("-", "")],
                relationships=[
                    EngineeringRelationship(
                        target_id=platform_id,
                        relationship_type=RelationshipType.COMPATIBLE_WITH,
                    )
                ],
                evidence=[EvidenceRecord(
                    source_id=self.source.source_id,
                    confidence=ConfidenceLevel.HIGH,
                    description=f"QuickSpecs processor table",
                    original_text_snippet=match.group(0)[:100],
                )],
            )
            processors.append(proc)

            self.delta_changes.append(DeltaChange(
                change_type=DeltaChangeType.NEW_OBJECT,
                object_id=proc.id,
                new_value=proc.title,
            ))

        logger.info(f"Extracted {len(processors)} processors")
        return processors

    # -------------------------------------------------------------------
    # Memory Extraction
    # -------------------------------------------------------------------

    def _extract_memory(self, text: str, platform: Optional[Platform]) -> List[BaseEngineeringObject]:
        """Extract memory specifications."""
        objects = []
        platform_id = platform.id if platform else "unknown"

        # Extract max memory capacity
        max_mem_match = re.search(r"up\s+to\s+(\d+)\s*(?:TB|GB)\s+(?:of\s+)?memory", text, re.IGNORECASE)
        if max_mem_match:
            max_mem = max_mem_match.group(1)
            unit = "TB" if "TB" in max_mem_match.group(0).upper() else "GB"

            constraint = CategoryLimit(
                id=f"{platform_id}/constraints/max-memory",
                title=f"Maximum Memory Capacity",
                description=f"Maximum supported memory: {max_mem} {unit}",
                vendor=platform.vendor if platform else "Unknown",
                solution_domain=platform.solution_domain if platform else "Unknown",
                product_family=platform.product_family if platform else None,
                generation=platform.generation if platform else None,
                platform_id=platform.id if platform else None,
                limit_name="Maximum Memory",
                limit_value=int(max_mem),
                limit_unit=unit,
                target_category="Memory",
                relationships=[
                    EngineeringRelationship(
                        target_id=platform_id,
                        relationship_type=RelationshipType.CONTAINS,
                    )
                ],
                evidence=[EvidenceRecord(
                    source_id=self.source.source_id,
                    confidence=ConfidenceLevel.HIGH,
                    description="QuickSpecs memory section",
                    original_text_snippet=max_mem_match.group(0),
                )],
            )
            objects.append(constraint)
            self.delta_changes.append(DeltaChange(
                change_type=DeltaChangeType.NEW_OBJECT,
                object_id=constraint.id,
                new_value=f"Max memory: {max_mem} {unit}",
            ))

        # Extract DIMM slot count
        dimm_match = re.search(r"(\d+)\s*DIMM\s*slots", text, re.IGNORECASE)
        if dimm_match:
            dimm_count = int(dimm_match.group(1))
            constraint = CategoryLimit(
                id=f"{platform_id}/constraints/dimm-slots",
                title="DIMM Slot Count",
                description=f"Total DIMM slots: {dimm_count}",
                vendor=platform.vendor if platform else "Unknown",
                solution_domain=platform.solution_domain if platform else "Unknown",
                product_family=platform.product_family if platform else None,
                generation=platform.generation if platform else None,
                platform_id=platform.id if platform else None,
                limit_name="DIMM Slots",
                limit_value=dimm_count,
                limit_unit="slots",
                target_category="Memory",
                relationships=[
                    EngineeringRelationship(
                        target_id=platform_id,
                        relationship_type=RelationshipType.CONTAINS,
                    )
                ],
                evidence=[EvidenceRecord(
                    source_id=self.source.source_id,
                    confidence=ConfidenceLevel.HIGH,
                    original_text_snippet=dimm_match.group(0),
                )],
            )
            objects.append(constraint)

        # Extract DDR types supported
        ddr_match = re.search(r"DDR(\d)\s+(?:speed|memory|RDIMM|LRDIMM)", text, re.IGNORECASE)
        if ddr_match:
            ddr_gen = ddr_match.group(1)
            mem_component = Component(
                id=f"{platform_id}/components/memory-ddr{ddr_gen}",
                title=f"DDR{ddr_gen} Memory",
                description=f"DDR{ddr_gen} memory support",
                vendor=platform.vendor if platform else "Unknown",
                solution_domain=platform.solution_domain if platform else "Unknown",
                product_family=platform.product_family if platform else None,
                generation=platform.generation if platform else None,
                platform_id=platform.id if platform else None,
                component_category="Memory",
                capabilities=[f"DDR{ddr_gen}"],
                relationships=[
                    EngineeringRelationship(
                        target_id=platform_id,
                        relationship_type=RelationshipType.COMPATIBLE_WITH,
                    )
                ],
                evidence=[EvidenceRecord(
                    source_id=self.source.source_id,
                    confidence=ConfidenceLevel.HIGH,
                )],
            )
            objects.append(mem_component)

        return objects

    # -------------------------------------------------------------------
    # Storage Extraction
    # -------------------------------------------------------------------

    def _extract_storage(self, text: str, platform: Optional[Platform]) -> List[BaseEngineeringObject]:
        """Extract storage / drive cage specifications."""
        objects = []
        platform_id = platform.id if platform else "unknown"

        # Extract max drive counts
        drive_patterns = [
            (r"up\s+to\s+(\d+)\s*SFF", "SFF Drives"),
            (r"up\s+to\s+(\d+)\s*LFF", "LFF Drives"),
            (r"up\s+to\s+(\d+)\s*EDSFF", "EDSFF Drives"),
            (r"up\s+to\s+(\d+)\s*NVMe", "NVMe Drives"),
        ]

        for pattern, name in drive_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                count = int(match.group(1))
                constraint = CategoryLimit(
                    id=f"{platform_id}/constraints/max-{name.lower().replace(' ', '-')}",
                    title=f"Maximum {name}",
                    description=f"Supports up to {count} {name}",
                    vendor=platform.vendor if platform else "Unknown",
                    solution_domain=platform.solution_domain if platform else "Unknown",
                    product_family=platform.product_family if platform else None,
                    generation=platform.generation if platform else None,
                    platform_id=platform.id if platform else None,
                    limit_name=f"Maximum {name}",
                    limit_value=count,
                    limit_unit="drives",
                    target_category="Drive",
                    relationships=[
                        EngineeringRelationship(
                            target_id=platform_id,
                            relationship_type=RelationshipType.CONTAINS,
                        )
                    ],
                    evidence=[EvidenceRecord(
                        source_id=self.source.source_id,
                        confidence=ConfidenceLevel.HIGH,
                        original_text_snippet=match.group(0),
                    )],
                )
                objects.append(constraint)
                self.delta_changes.append(DeltaChange(
                    change_type=DeltaChangeType.NEW_OBJECT,
                    object_id=constraint.id,
                    new_value=f"Max {name}: {count}",
                ))

        return objects

    # -------------------------------------------------------------------
    # Networking Extraction
    # -------------------------------------------------------------------

    def _extract_networking(self, text: str, platform: Optional[Platform]) -> List[Component]:
        """Extract networking/OCP/NIC information."""
        components = []
        platform_id = platform.id if platform else "unknown"

        # Extract OCP slots
        ocp_match = re.search(r"OCP\s+(\d+\.?\d*)\s+Slot", text, re.IGNORECASE)
        if ocp_match:
            ocp_ver = ocp_match.group(1)
            nic = Component(
                id=f"{platform_id}/components/ocp-{ocp_ver}",
                title=f"OCP {ocp_ver} Network Adapter Slot",
                description=f"OCP {ocp_ver} compliant network adapter slot",
                vendor=platform.vendor if platform else "Unknown",
                solution_domain=platform.solution_domain if platform else "Unknown",
                product_family=platform.product_family if platform else None,
                generation=platform.generation if platform else None,
                platform_id=platform.id if platform else None,
                component_category="NIC",
                capabilities=[f"OCP {ocp_ver}", "Ethernet"],
                relationships=[
                    EngineeringRelationship(
                        target_id=platform_id,
                        relationship_type=RelationshipType.CONTAINS,
                    )
                ],
                evidence=[EvidenceRecord(
                    source_id=self.source.source_id,
                    confidence=ConfidenceLevel.MEDIUM,
                )],
            )
            components.append(nic)

        return components

    # -------------------------------------------------------------------
    # GPU/Accelerator Extraction
    # -------------------------------------------------------------------

    def _extract_gpus(self, text: str, platform: Optional[Platform]) -> List[Component]:
        """Extract GPU/accelerator information."""
        components = []
        platform_id = platform.id if platform else "unknown"

        # Pattern for NVIDIA GPUs
        gpu_patterns = [
            r"NVIDIA\s+([\w\s]+?)\s+(\d+)GB\s+PCIe",
            r"NVIDIA\s+(RTX\s+[\w\s]+?)\s+(\d+)GB",
            r"NVIDIA\s+(A\d+)\s+(\d+)GB",
            r"NVIDIA\s+(H\d+\w*)\s+(\d+)GB",
            r"NVIDIA\s+(L\d+\w*)\s+(\d+)GB",
        ]

        seen_gpus = set()
        for pattern in gpu_patterns:
            for match in re.finditer(pattern, text):
                model = match.group(1).strip()
                memory = match.group(2)
                key = f"{model}-{memory}"
                if key in seen_gpus:
                    continue
                seen_gpus.add(key)

                gpu_id = f"{platform_id}/components/gpu-{model.lower().replace(' ', '-')}"
                gpu = Component(
                    id=gpu_id,
                    title=f"NVIDIA {model} {memory}GB",
                    description=f"NVIDIA {model} with {memory}GB memory",
                    vendor="NVIDIA",
                    solution_domain=platform.solution_domain if platform else "Unknown",
                    product_family=platform.product_family if platform else None,
                    generation=platform.generation if platform else None,
                    platform_id=platform.id if platform else None,
                    component_category="GPU",
                    capabilities=["GPU", "AI", "PCIe Gen5"],
                    attributes=[
                        EngineeringAttribute(name="GPU Memory", value=int(memory), unit="GB"),
                    ],
                    relationships=[
                        EngineeringRelationship(
                            target_id=platform_id,
                            relationship_type=RelationshipType.COMPATIBLE_WITH,
                        )
                    ],
                    tags=["gpu", "nvidia", "accelerator", "ai"],
                    evidence=[EvidenceRecord(
                        source_id=self.source.source_id,
                        confidence=ConfidenceLevel.HIGH,
                        original_text_snippet=match.group(0),
                    )],
                )
                components.append(gpu)
                self.delta_changes.append(DeltaChange(
                    change_type=DeltaChangeType.NEW_OBJECT,
                    object_id=gpu_id,
                    new_value=f"NVIDIA {model} {memory}GB",
                ))

        logger.info(f"Extracted {len(components)} GPU/accelerators")
        return components

    # -------------------------------------------------------------------
    # Rules & Constraints Extraction
    # -------------------------------------------------------------------

    def _extract_rules(self, text: str, platform: Optional[Platform]) -> List[Rule]:
        """Extract engineering rules from notes, warnings, and constraints."""
        rules = []
        platform_id = platform.id if platform else "unknown"

        # Extract notes and warnings
        note_patterns = [
            (r"[Nn]ote[s]?:\s*[-−–•]\s*(.+?)(?:\n|$)", RuleSeverity.INFO),
            (r"[Ww]arning[s]?:\s*[-−–•]\s*(.+?)(?:\n|$)", RuleSeverity.WARNING),
            (r"[Ii]mportant:\s*(.+?)(?:\n|$)", RuleSeverity.WARNING),
            (r"[Rr]equires?\s+(.+?firmware.+?)(?:\n|$)", RuleSeverity.ERROR),
            (r"[-−–•]\s*(Requires\s+.+?)(?:\n|$)", RuleSeverity.ERROR),
            (r"[-−–•]\s*(Cannot\s+be\s+selected\s+with.+?)(?:\n|$)", RuleSeverity.ERROR),
            (r"[-−–•]\s*(Must\s+be\s+selected\s+with.+?)(?:\n|$)", RuleSeverity.ERROR),
            (r"[-−–•]\s*(If\s+.+?then\s+.+?)(?:\n|$)", RuleSeverity.WARNING),
        ]

        seen_rules = set()
        rule_count = 0

        for pattern, severity in note_patterns:
            for match in re.finditer(pattern, text):
                rule_text = match.group(1).strip()
                if len(rule_text) < 15 or rule_text in seen_rules:
                    continue
                seen_rules.add(rule_text)
                
                is_negated = self._negation_shield(rule_text)
                target_text = self._strip_conditional(rule_text)
                
                # Splitting targets
                raw_targets = re.split(r',|\sand\s|\sor\s|&', target_text, flags=re.IGNORECASE)
                targets = [t.strip() for t in raw_targets if len(t.strip()) > 2]

                rule_count += 1

                rule = Rule(
                    id=f"{platform_id}/rules/rule-{rule_count:03d}",
                    title=f"Engineering Rule {rule_count}",
                    description=rule_text[:200],
                    vendor=platform.vendor if platform else "Unknown",
                    solution_domain=platform.solution_domain if platform else "Unknown",
                    product_family=platform.product_family if platform else None,
                    generation=platform.generation if platform else None,
                    platform_id=platform.id if platform else None,
                    scope="Platform",
                    severity=severity,
                    confidence=ConfidenceLevel.HIGH,
                    applicable_objects=[platform_id],
                    expected_outcome=rule_text,
                    negated=is_negated,
                    dependency_targets=targets,
                    evidence=[EvidenceRecord(
                        source_id=self.source.source_id,
                        confidence=ConfidenceLevel.HIGH,
                        original_text_snippet=rule_text[:200],
                    )],
                )
                rules.append(rule)

        # PARALLEL AI STUDIO ANALYSIS (Quality Assurance)
        import concurrent.futures
        
        logger.info("Spawning parallel AI tasks for rule extraction...")
        llm_rules = []
        critic_rules = []
        
        # Analyze first 15000 chars for rules to save tokens while capturing key constraints
        chunk = text[:15000]
        
        # Sequential extraction for AI rules to prevent OAuth browser race conditions
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future_primary = executor.submit(self.llm_client.extract_rules, chunk)
            future_critic = executor.submit(self.llm_client.critic_review_rules, chunk)
            
            try:
                llm_rules = future_primary.result(timeout=45)
            except Exception as e:
                logger.error(f"Primary LLM rule extraction timed out or failed: {e}")
                
            try:
                critic_rules = future_critic.result(timeout=45)
            except Exception as e:
                logger.error(f"Critic LLM rule extraction timed out or failed: {e}")
                
        merged_llm_rules = llm_rules + critic_rules
        logger.info(f"LLM extraction returned {len(merged_llm_rules)} AI-generated rules.")

        # Process and deduplicate AI-generated rules
        for r_dict in merged_llm_rules:
            rule_text = r_dict.get("rule_text", "").strip()
            if not rule_text or rule_text in seen_rules:
                continue
            seen_rules.add(rule_text)
            
            sev_str = r_dict.get("severity", "Info").upper()
            severity = RuleSeverity.INFO
            if sev_str == "WARNING": severity = RuleSeverity.WARNING
            elif sev_str == "ERROR": severity = RuleSeverity.ERROR
            
            # MCP CROSS-REFERENCING
            mcp_evidence = []
            try:
                mcp_results = self.mcp_client.search(rule_text[:50])
                for mcp_res in mcp_results[:2]: # Take top 2 matches
                    mcp_evidence.append(EvidenceRecord(
                        source_id=mcp_res,
                        confidence=ConfidenceLevel.MEDIUM,
                        description="Obsidian MCP cross-reference match",
                    ))
            except Exception as e:
                logger.warning(f"MCP search failed for rule: {e}")

            rule_count += 1
            
            evidence = [EvidenceRecord(
                source_id=self.source.source_id,
                confidence=ConfidenceLevel.MEDIUM,
                description="AI-generated rule from text chunk",
                original_text_snippet=rule_text,
            )]
            evidence.extend(mcp_evidence)

            rule = Rule(
                id=f"{platform_id}/rules/rule-{rule_count:03d}",
                title=f"Engineering Rule {rule_count}",
                description=rule_text[:200],
                vendor=platform.vendor if platform else "Unknown",
                solution_domain=platform.solution_domain if platform else "Unknown",
                product_family=platform.product_family if platform else None,
                generation=platform.generation if platform else None,
                platform_id=platform.id if platform else None,
                scope="Platform",
                severity=severity,
                confidence=ConfidenceLevel.MEDIUM,
                applicable_objects=[platform_id],
                expected_outcome=rule_text,
                negated=False,
                dependency_targets=r_dict.get("targets", []),
                evidence=evidence,
            )
            rules.append(rule)

        logger.info(f"Extracted total {len(rules)} engineering rules")
        return rules

    # -------------------------------------------------------------------
    # Power Supply Extraction
    # -------------------------------------------------------------------

    def _extract_power(self, text: str, platform: Optional[Platform]) -> List[Component]:
        """Extract power supply specifications."""
        components = []
        platform_id = platform.id if platform else "unknown"

        psu_pattern = re.compile(r"(\d{3,4})\s*W\s+(?:Flex\s+Slot|Power\s+Supply)", re.IGNORECASE)
        seen_watts = set()

        for match in psu_pattern.finditer(text):
            watts = match.group(1)
            if watts in seen_watts:
                continue
            seen_watts.add(watts)

            psu = Component(
                id=f"{platform_id}/components/psu-{watts}w",
                title=f"{watts}W Power Supply",
                description=f"{watts}W Flex Slot Power Supply",
                vendor=platform.vendor if platform else "Unknown",
                solution_domain=platform.solution_domain if platform else "Unknown",
                product_family=platform.product_family if platform else None,
                generation=platform.generation if platform else None,
                platform_id=platform.id if platform else None,
                component_category="PSU",
                attributes=[
                    EngineeringAttribute(name="Wattage", value=int(watts), unit="W"),
                ],
                relationships=[
                    EngineeringRelationship(
                        target_id=platform_id,
                        relationship_type=RelationshipType.COMPATIBLE_WITH,
                    )
                ],
                evidence=[EvidenceRecord(
                    source_id=self.source.source_id,
                    confidence=ConfidenceLevel.HIGH,
                    original_text_snippet=match.group(0),
                )],
            )
            components.append(psu)

        return components

    # -------------------------------------------------------------------
    # Structured Tabular Extraction (via TableParser)
    # -------------------------------------------------------------------

    # -------------------------------------------------------------------
    # Component Category Taxonomy — comprehensive classification
    # -------------------------------------------------------------------

    COMPONENT_CATEGORY_MAP = [
        # (keywords_list, category, subcategory)  — checked in priority order
        # Memory
        (["Memory", "DIMM", "RDIMM", "LRDIMM", "DDR5", "DDR4", "RAM", "Smart Memory"], "Memory", "DIMM"),
        # Storage - Controllers
        (["Controller", "Smart Array", "MR416", "MR216", "MR932", "RAID", "HBA", "SR932", "VROC"], "Storage", "Controller"),
        # Storage - Boot devices
        (["NS204", "Boot Optimized", "Boot Device", "MicroServer Boot"], "Storage", "Boot Device"),
        # Storage - Drives
        (["Drive", "SSD", "HDD", "NVMe", "EDSFF", "E3.S", "Solid State", "Hard Disk", "Midline"], "Storage", "Drive"),
        # Storage - Battery/Capacitor
        (["Battery", "BBWC", "FBWC", "Smart Storage Battery", "Capacitor Pack", "Energy Pack"], "Storage", "Battery Backup"),
        # Networking - NICs
        (["Adapter", "NIC", "OCP", "Ethernet", "InfiniBand", "CX7", "CX6", "ConnectX", "BCM57", "I350", "E810", "BASE-T"], "Networking", "NIC"),
        # Networking - Optics
        (["Optic", "Transceiver", "SFP", "QSFP", "OSFP", "DAC Cable", "AOC"], "Networking", "Optics"),
        # Networking - Switches (for Synergy-type)
        (["Switch", "Interconnect", "Virtual Connect", "Fabric Module"], "Networking", "Switch/Interconnect"),
        # GPU / Accelerators
        (["GPU", "Accelerator", "NVIDIA", "Tesla", "A100", "H100", "H200", "L40", "L4", "RTX", "Instinct", "Gaudi"], "Accelerator", "GPU"),
        # Power
        (["Power Supply", "PSU", "Flex Slot", "Power Cable", "PDU", "UPS"], "Power", "PSU"),
        # Power - DC
        (["DC Power", "-48V", "DC PSU", "HVDC"], "Power", "DC Power"),
        # Thermal
        (["Heatsink", "Heat Sink", "Cooling", "Cold Plate", "DLC", "Direct Liquid"], "Thermal", "Heatsink"),
        (["Fan", "Cooling Fan", "Fan Module", "Performance Fan"], "Thermal", "Fan"),
        # Chassis
        (["Bezel", "Front Panel", "Bezel Kit", "Bezel Lock"], "Chassis", "Bezel"),
        (["Rail", "Rack Rail", "Friction Rail", "Easy Install Rail", "Slide Rail"], "Chassis", "Rail Kit"),
        (["Blank", "Filler", "DIMM Blank", "Bay Blank", "Drive Blank"], "Chassis", "Blank/Filler"),
        (["Chassis", "Enclosure", "Frame"], "Chassis", "Enclosure"),
        # Infrastructure
        (["Riser", "Riser Kit", "Riser Card", "Secondary Riser"], "Infrastructure", "Riser"),
        (["Cable Kit", "Cable", "SAS Cable", "Power Cable", "Signal Cable", "Enablement Cable"], "Infrastructure", "Cable"),
        (["Enablement", "Enable Kit", "Bay Enable", "Cage Enable", "Midplane"], "Infrastructure", "Enablement Kit"),
        (["Serial Port", "DisplayPort", "VGA", "USB", "I/O Module"], "Infrastructure", "I/O Port"),
        (["Optical Drive", "DVD", "DVD-ROM", "DVD-RW", "Media Bay"], "Infrastructure", "Optical Drive"),
        # Security
        (["TPM", "Trusted Platform", "Security", "Bezel Lock", "Intrusion", "iDevID"], "Security", "TPM/Security"),
        # Management
        (["iLO", "Lights Out", "Management", "Compute Ops", "Insight", "OneView"], "Management", "Management Software"),
        # Services (non-hardware SKUs)
        (["Service", "Support", "Warranty", "Tech Care", "Install", "Startup", "Consulting"], "Services", "Support/Warranty"),
    ]

    def _classify_component(self, description: str) -> tuple:
        """Classify a component description into (category, subcategory) using keyword scoring."""
        desc_upper = description.upper()
        
        best_score = 0
        best_cat = "Accessory"
        best_subcat = "General"
        
        for keywords, category, subcategory in self.COMPONENT_CATEGORY_MAP:
            score = 0
            for kw in keywords:
                if kw.upper() in desc_upper:
                    # Longer keywords get higher scores (more specific match)
                    score += len(kw)
            if score > best_score:
                best_score = score
                best_cat = category
                best_subcat = subcategory
        
        return best_cat, best_subcat

    def _process_structured_components(self, structured_components: List[Dict[str, Any]], platform: Optional[Platform]) -> List[BaseEngineeringObject]:
        """Convert structured dictionary rows from TableParser into Component + SKU objects and CategoryLimits."""
        objects = []
        platform_id = platform.id if platform else "unknown"
        seen_skus = set()

        for data in structured_components:
            sku = data["sku"]
            if sku in seen_skus:
                continue
            seen_skus.add(sku)

            desc = data["description"]
            brackets = data["brackets"]
            qty = data["default_qty"]

            # Use brackets as tags/capabilities
            capabilities = [b.strip("()[]") for b in brackets if len(b) < 10]
            
            # Classify with comprehensive taxonomy
            cat, subcat = self._classify_component(desc)
            
            # Extract category limits (e.g. "Maximum 2 Risers")
            if subcat and subcat != "General":
                limit_match = re.search(r'Maximum\s+(\d+)\s+' + re.escape(subcat), desc, re.IGNORECASE)
                if not limit_match:
                    # Also try with category name
                    limit_match = re.search(r'Maximum\s+(?:quantity\s+)?(\d+)', desc, re.IGNORECASE)
                if limit_match:
                    limit_qty = int(limit_match.group(1))
                    cl = CategoryLimit(
                        id=f"{platform_id}/limits/max-{subcat.lower().replace('/', '-').replace(' ', '-')}",
                        title=f"Max {subcat}",
                        limit_name=f"Maximum {subcat}",
                        limit_value=limit_qty,
                        target_category=cat,
                        target_subcategory=subcat,
                        vendor=platform.vendor if platform else "Unknown",
                        solution_domain=platform.solution_domain if platform else "Unknown",
                        product_family=platform.product_family if platform else None,
                        generation=platform.generation if platform else None,
                        platform_id=platform.id if platform else None,
                        relationships=[EngineeringRelationship(target_id=platform_id, relationship_type=RelationshipType.CONTAINS)]
                    )
                    objects.append(cl)
            
            # Determine packaging type and kit inclusion
            pkg_type = PackagingType.STANDALONE
            inclusive_qty = None
            if re.search(r'\b(?:Kit|Bundle)\b', desc, re.IGNORECASE):
                pkg_type = PackagingType.BUNDLE
                qty_match = re.search(r'(\d+)x', desc, re.IGNORECASE)
                if qty_match:
                    inclusive_qty = int(qty_match.group(1))
            elif sku.endswith("-001"):
                pkg_type = PackagingType.SPARE
            
            attributes = []
            if qty > 0:
                attributes.append(EngineeringAttribute(name="Default Quantity", value=qty))

            # Create the engineering Component
            comp_id = f"{platform_id}/components/{sku.lower()}"
            comp = Component(
                id=comp_id,
                title=f"{sku} - {desc[:50]}..." if len(desc) > 50 else f"{sku} - {desc}",
                description=desc,
                vendor=platform.vendor if platform else "Unknown",
                solution_domain=platform.solution_domain if platform else "Unknown",
                product_family=platform.product_family if platform else None,
                generation=platform.generation if platform else None,
                platform_id=platform.id if platform else None,
                component_category=cat,
                component_subcategory=subcat,
                packaging_type=pkg_type,
                inclusive_qty=inclusive_qty,
                capabilities=capabilities,
                attributes=attributes,
                relationships=[
                    EngineeringRelationship(
                        target_id=platform_id,
                        relationship_type=RelationshipType.COMPATIBLE_WITH,
                    )
                ],
                evidence=[EvidenceRecord(
                    source_id=self.source.source_id,
                    confidence=ConfidenceLevel.HIGH,
                    description=f"Extracted from Table on page {data.get('page')}",
                )]
            )
            objects.append(comp)
            
            # Create a paired SKU (commercial identity) linked to the Component
            sku_obj = SKU(
                id=f"{platform_id}/skus/{sku.lower()}",
                title=f"SKU {sku}",
                description=desc,
                part_number=sku,
                vendor=platform.vendor if platform else "Unknown",
                solution_domain=platform.solution_domain if platform else "Unknown",
                product_family=platform.product_family if platform else None,
                generation=platform.generation if platform else None,
                platform_id=platform.id if platform else None,
                component_id=comp_id,
                packaging_type=pkg_type,
                inclusive_qty=inclusive_qty,
                relationships=[
                    EngineeringRelationship(
                        target_id=comp_id,
                        relationship_type=RelationshipType.HAS_SKU,
                    ),
                    EngineeringRelationship(
                        target_id=platform_id,
                        relationship_type=RelationshipType.COMPATIBLE_WITH,
                    ),
                ],
                evidence=[EvidenceRecord(
                    source_id=self.source.source_id,
                    confidence=ConfidenceLevel.HIGH,
                    description=f"SKU extracted from Table on page {data.get('page')}",
                )]
            )
            objects.append(sku_obj)
            
            self.delta_changes.append(DeltaChange(
                change_type=DeltaChangeType.NEW_COMPONENT,
                object_id=comp.id,
                new_value=sku,
            ))
            self.delta_changes.append(DeltaChange(
                change_type=DeltaChangeType.NEW_SKU,
                object_id=sku_obj.id,
                new_value=sku,
            ))

        logger.info(f"Processed {len(objects)} structured tabular components.")
        return objects

    # -------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------

    def _normalize_text(self, text: str) -> str:
        """Stage 1: Normalize invisible PDF typography and Unicode artifacts."""
        text = text.replace('\u2212', '-')  # Minus sign
        text = text.replace('\u2013', '-')  # En-dash
        text = text.replace('\u2014', '-')  # Em-dash
        text = text.replace('\u2022', '*')  # Bullet point
        text = text.replace('\u201c', '"').replace('\u201d', '"')
        text = text.replace('\u2018', "'").replace('\u2019', "'")
        text = text.replace('\u00ae', '(R)')
        text = text.replace('\u2122', '(TM)')
        text = text.replace('\u00a0', ' ')
        return text

    def _negation_shield(self, rule_text: str) -> bool:
        """Returns True if the rule contains negation phrasing that should reverse/discard positive triggers."""
        negation_patterns = [r"no longer requires", r"not required", r"is an embedded feature", r"no longer needs"]
        return any(re.search(p, rule_text, re.IGNORECASE) for p in negation_patterns)

    def _strip_conditional(self, rule_text: str) -> str:
        """Strips leading conditionals like 'If X, then Y' down to just 'Y' for the dependency target."""
        then_match = re.search(r'\bthen\s+(.*)', rule_text, re.IGNORECASE)
        if then_match:
            return then_match.group(1).strip()
        return rule_text

    def _extract_topology(self, text: str, platform: Optional[Platform]) -> None:
        """Extract spatial topology and slot mappings."""
        if not platform: return
        
        # Look for typical Mezzanine to Bay topology mappings
        # e.g. "Mezzanine Slot 1 connects to Bay 1 and Bay 4"
        topo_pattern = re.compile(r"(Mezzanine\s+Slot\s+\d+).*?(Bay\s+\d+).*?(Bay\s+\d+)", re.IGNORECASE)
        slot_count = 0
        for match in topo_pattern.finditer(text):
            source_slot = match.group(1).strip()
            target_1 = match.group(2).strip()
            target_2 = match.group(3).strip()
            
            slot_count += 1
            mapping_id = f"{platform.id}/slot-mappings/slot-{slot_count:03d}"
            
            mapping = SlotMapping(
                id=mapping_id,
                title=f"Slot Mapping: {source_slot}",
                vendor=platform.vendor,
                solution_domain=platform.solution_domain,
                platform_id=platform.id,
                source_slot=source_slot,
                target_bays=[target_1, target_2],
                redundancy_link=target_2,
                evidence=[EvidenceRecord(
                    source_id=self.source.source_id,
                    confidence=ConfidenceLevel.HIGH,
                    original_text_snippet=match.group(0)[:100],
                )],
            )
            self.extracted_objects.append(mapping)
            platform.slot_mapping_ids.append(mapping_id)

    def _extract_description(self, text: str) -> str:
        """Extract product description from introductory text."""
        patterns = [
            r"(The HPE ProLiant.+?(?:forward|growth|workloads)\.)",
            r"(The HPE Alletra.+?(?:forward|growth|workloads)\.)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                desc = match.group(1).replace("\n", " ").strip()
                return desc[:500]
        return ""

    def _extract_form_factor(self, text: str) -> Optional[str]:
        """Extract form factor."""
        match = re.search(r"(\d+U)\s+rack", text, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def _extract_chassis_types(self, text: str) -> List[str]:
        """Extract chassis type variants."""
        chassis = []
        patterns = [
            r"(SFF\s+CTO\s+Server)",
            r"(\d+SFF\s+CTO\s+Server)",
            r"(\d+LFF\s+CTO\s+Server)",
            r"(EDSFF\s+CTO\s+Server)",
        ]
        seen = set()
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                ct = match.group(1).strip()
                if ct not in seen:
                    seen.add(ct)
                    chassis.append(ct)
        return chassis

    def _extract_capabilities(self, text: str) -> List[str]:
        """Extract engineering capabilities mentioned in the document."""
        capability_keywords = {
            "PCIe Gen5": r"PCIe\s*Gen\s*5",
            "DDR5": r"DDR5",
            "NVMe": r"NVMe",
            "GPU Support": r"GPU|accelerator",
            "AI Ready": r"AI[- ](?:driven|ready|optimized|inference|training)",
            "Direct Liquid Cooling": r"[Dd]irect\s+[Ll]iquid\s+[Cc]ooling|DLC",
            "Silicon Root of Trust": r"Silicon\s+Root\s+of\s+Trust",
            "iLO 7": r"iLO\s*7",
            "OCP 3.0": r"OCP\s*3\.0",
            "Redundant Power": r"[Rr]edundant\s+[Pp]ower",
            "Hot Plug": r"[Hh]ot[- ][Pp]lug",
            "UEFI Secure Boot": r"UEFI\s+Secure\s+Boot",
        }
        found = []
        for cap, pattern in capability_keywords.items():
            if re.search(pattern, text, re.IGNORECASE):
                found.append(cap)
        return found

    def _extract_workload_tags(self, text: str) -> List[str]:
        """Extract workload suitability tags."""
        workload_keywords = {
            "ai": r"\bAI\b",
            "virtualization": r"VMware|vSphere|[Vv]irtualiz",
            "database": r"SQL\s+Server|Oracle|database",
            "hpc": r"\bHPC\b|[Hh]igh\s+[Pp]erformance\s+[Cc]omputing",
            "vdi": r"\bVDI\b|[Vv]irtual\s+[Dd]esktop",
            "sap": r"\bSAP\b",
            "kubernetes": r"Kubernetes|K8s",
            "cloud": r"[Cc]loud|hybrid",
        }
        found = []
        for tag, pattern in workload_keywords.items():
            if re.search(pattern, text):
                found.append(tag)
        return found
