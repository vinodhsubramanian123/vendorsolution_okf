"""
OKF Reader — Parses existing OKF Markdown files back into Pydantic models.

Governs: Architectural requirement for bidirectional sync (Gap 13 from audit)

This is essential for bootstrapping the in-memory graph from an existing
repository on startup. Without this, the system cannot be restarted without
losing all knowledge.
"""

import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from ikp_platform.core.ontology.models import (
    BaseEngineeringObject,
    EngineeringObjectType,
    EngineeringRelationship,
    RelationshipType,
    EngineeringAttribute,
    EvidenceRecord,
    LifecycleStatus,
    ConfidenceLevel,
    Rule,
    RuleSeverity,
    Constraint,
    Component,
    Platform,
    SKU,
    Workload,
    CategoryLimit,
    SlotMapping,
    SolutionCategory,
    Variant,
    Configuration,
    PackagingType,
)


class OKFReader:
    """Parses OKF Markdown files and reconstructs Pydantic engineering objects."""

    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)

    def load_all(self) -> List[BaseEngineeringObject]:
        """
        Recursively scan the repository and parse all concept files.
        Skips reserved files (index.md, log.md).
        """
        objects = []
        if not self.repository_path.exists():
            return objects

        for md_file in sorted(self.repository_path.rglob("*.md")):
            if md_file.name in ("index.md", "log.md"):
                continue
            obj = self._parse_file(md_file)
            if obj:
                objects.append(obj)

        return objects

    def _parse_file(self, file_path: Path) -> Optional[BaseEngineeringObject]:
        """Parse a single OKF Markdown file into a Pydantic model."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract frontmatter
        frontmatter, body = self._split_frontmatter(content)
        if not frontmatter:
            return None

        obj_type_str = frontmatter.get("type")
        if not obj_type_str:
            return None

        # Map type string to enum
        try:
            obj_type = EngineeringObjectType(obj_type_str)
        except ValueError:
            # Unknown type — treat as generic
            obj_type = EngineeringObjectType.COMPONENT

        # Extract relationships from body cross-links
        relationships = self._extract_relationships(body)

        # Extract evidence from Citations section
        evidence = self._extract_evidence(body)

        # Extract structured attributes from attr_* frontmatter keys
        attributes = []
        attr_keys = [k for k in frontmatter if k.startswith("attr_")]
        for key in attr_keys:
            attr_name = key[5:].replace("_", " ").title()
            unit_key = f"{key}_unit"
            attributes.append(EngineeringAttribute(
                name=attr_name,
                value=frontmatter[key],
                unit=frontmatter.get(unit_key),
            ))

        # Parse lifecycle status
        lifecycle_str = frontmatter.get("lifecycle_status", "Unknown")
        try:
            lifecycle = LifecycleStatus(lifecycle_str)
        except ValueError:
            lifecycle = LifecycleStatus.UNKNOWN

        # Parse timestamp
        ts = frontmatter.get("timestamp")
        timestamp = None
        if ts:
            try:
                if isinstance(ts, datetime):
                    timestamp = ts
                else:
                    timestamp = datetime.fromisoformat(ts.rstrip("Z"))
            except (ValueError, AttributeError):
                timestamp = None

        # Derive ID from frontmatter if available, otherwise fallback to file path
        relative = file_path.relative_to(self.repository_path)
        obj_id = frontmatter.get("id", str(relative.with_suffix("")))

        # Build common kwargs
        kwargs = {
            "id": obj_id,
            "type": obj_type,
            "title": frontmatter.get("title"),
            "description": frontmatter.get("description"),
            "vendor": frontmatter.get("vendor"),
            "solution_domain": frontmatter.get("solution_domain"),
            "product_family": frontmatter.get("product_family"),
            "generation": frontmatter.get("generation"),
            "platform_id": frontmatter.get("platform_id"),
            "lifecycle_status": lifecycle,
            "attributes": attributes,
            "relationships": relationships,
            "capabilities": frontmatter.get("capabilities", []),
            "tags": frontmatter.get("tags", []),
            "evidence": evidence,
        }

        # Instantiate specialized types
        if obj_type == EngineeringObjectType.RULE:
            severity_str = frontmatter.get("severity", "Info")
            try:
                severity = RuleSeverity(severity_str)
            except ValueError:
                severity = RuleSeverity.INFO

            confidence_str = frontmatter.get("confidence", "Unverified")
            try:
                confidence = ConfidenceLevel(confidence_str)
            except ValueError:
                confidence = ConfidenceLevel.UNVERIFIED

            return Rule(
                **kwargs,
                scope=frontmatter.get("scope"),
                severity=severity,
                confidence=confidence,
                applicable_objects=frontmatter.get("applicable_objects", []),
                expected_outcome=self._extract_section(body, "Expected Outcome"),
                trigger_conditions=self._extract_list_section(body, "Trigger Conditions"),
                version=frontmatter.get("rule_version", 1),
            )

        if obj_type == EngineeringObjectType.CONSTRAINT:
            return Constraint(
                **kwargs,
                limit_name=frontmatter.get("limit_name", ""),
                limit_value=frontmatter.get("limit_value"),
                limit_unit=frontmatter.get("limit_unit"),
            )

        if obj_type == EngineeringObjectType.COMPONENT:
            return Component(
                **kwargs,
                component_category=frontmatter.get("component_category"),
                component_subcategory=frontmatter.get("component_subcategory"),
            )

        if obj_type == EngineeringObjectType.PLATFORM:
            return Platform(
                **kwargs,
                parent_platform_id=frontmatter.get("parent_platform_id"),
                platform_sku=frontmatter.get("platform_sku"),
            )

        if obj_type == EngineeringObjectType.SKU:
            pkg_type_str = frontmatter.get("packaging_type")
            pkg_type = PackagingType(pkg_type_str) if pkg_type_str else PackagingType.STANDALONE
            return SKU(
                **kwargs,
                part_number=frontmatter.get("part_number", ""),
                price=frontmatter.get("price"),
                currency=frontmatter.get("currency"),
                component_id=frontmatter.get("component_id"),
                packaging_type=pkg_type,
            )

        if obj_type == EngineeringObjectType.WORKLOAD:
            return Workload(
                **kwargs,
                performance_requirements=frontmatter.get("performance_requirements", {}),
                capacity_requirements=frontmatter.get("capacity_requirements", {}),
            )

        if obj_type == EngineeringObjectType.CATEGORY_LIMIT:
            return CategoryLimit(
                **kwargs,
                limit_name=frontmatter.get("limit_name", ""),
                limit_value=frontmatter.get("limit_value"),
                limit_unit=frontmatter.get("limit_unit"),
                target_category=frontmatter.get("target_category"),
                target_subcategory=frontmatter.get("target_subcategory"),
            )

        if obj_type == EngineeringObjectType.SLOT_MAPPING:
            return SlotMapping(
                **kwargs,
                source_slot=frontmatter.get("source_slot", ""),
                target_bays=frontmatter.get("target_bays", []),
                redundancy_link=frontmatter.get("redundancy_link"),
                constraints=frontmatter.get("constraints", []),
            )

        if obj_type == EngineeringObjectType.SOLUTION_CATEGORY:
            return SolutionCategory(**kwargs)
            
        if obj_type == EngineeringObjectType.VARIANT:
            return Variant(
                **kwargs,
                base_platform_id=frontmatter.get("base_platform_id", ""),
                differentiators=frontmatter.get("differentiators", []),
            )
            
        if obj_type == EngineeringObjectType.CONFIGURATION:
            return Configuration(
                **kwargs,
                base_platform_id=frontmatter.get("base_platform_id", ""),
                included_components=frontmatter.get("included_components", []),
                validated=frontmatter.get("validated", False),
            )

        return BaseEngineeringObject(**kwargs)

    # -------------------------------------------------------------------
    # Parsing helpers
    # -------------------------------------------------------------------

    @staticmethod
    def _split_frontmatter(content: str):
        """Split an OKF file into (frontmatter_dict, body_str)."""
        if not content.startswith("---"):
            return {}, content

        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}, content

        try:
            fm = yaml.safe_load(parts[1]) or {}
        except yaml.YAMLError:
            fm = {}

        body = parts[2].strip()
        return fm, body

    @staticmethod
    def _extract_relationships(body: str) -> List[EngineeringRelationship]:
        """Extract relationships from the Markdown body's Relationships section."""
        relationships = []
        in_section = False

        for line in body.split("\n"):
            stripped = line.strip()
            if stripped.startswith("# Relationships"):
                in_section = True
                continue
            if stripped.startswith("# ") and in_section:
                break
            if in_section and stripped.startswith("- **"):
                # Parse: - **Requires**: [target_id](/target_id.md)
                try:
                    rel_type_str = stripped.split("**")[1]
                    # Extract target from markdown link
                    link_start = stripped.index("[") + 1
                    link_end = stripped.index("]")
                    target_id = stripped[link_start:link_end]

                    try:
                        rel_type = RelationshipType(rel_type_str)
                    except ValueError:
                        continue

                    relationships.append(EngineeringRelationship(
                        target_id=target_id,
                        relationship_type=rel_type,
                    ))
                except (IndexError, ValueError):
                    continue

        return relationships

    @staticmethod
    def _extract_evidence(body: str) -> List[EvidenceRecord]:
        """Extract evidence from the Citations section (OKF §8)."""
        evidence = []
        in_section = False

        for line in body.split("\n"):
            stripped = line.strip()
            if stripped.startswith("# Citations"):
                in_section = True
                continue
            if stripped.startswith("# ") and in_section:
                break
            if in_section and stripped.startswith("["):
                try:
                    # Parse: [1] [description](url) — _snippet_
                    # or:    [1] description
                    bracket_end = stripped.index("]", 1)
                    rest = stripped[bracket_end + 1:].strip()

                    desc = rest
                    url = None
                    snippet = None

                    if rest.startswith("["):
                        link_end = rest.index("]")
                        desc = rest[1:link_end]
                        if "(" in rest:
                            url_start = rest.index("(") + 1
                            url_end = rest.index(")")
                            url = rest[url_start:url_end]

                    if "— _" in rest and rest.endswith("_"):
                        snippet = rest.split("— _")[1].rstrip("_")

                    evidence.append(EvidenceRecord(
                        source_id=desc,
                        description=desc,
                        url=url,
                        original_text_snippet=snippet,
                    ))
                except (IndexError, ValueError):
                    continue

        return evidence

    @staticmethod
    def _extract_section(body: str, heading: str) -> str:
        """Extract text content under a specific heading."""
        lines = body.split("\n")
        in_section = False
        result = []
        for line in lines:
            stripped = line.strip()
            if stripped == f"# {heading}":
                in_section = True
                continue
            if stripped.startswith("# ") and in_section:
                break
            if in_section:
                result.append(line)
        return "\n".join(result).strip()

    @staticmethod
    def _extract_list_section(body: str, heading: str) -> List[str]:
        """Extract a bulleted list under a specific heading."""
        lines = body.split("\n")
        in_section = False
        result = []
        for line in lines:
            stripped = line.strip()
            if stripped == f"# {heading}":
                in_section = True
                continue
            if stripped.startswith("# ") and in_section:
                break
            if in_section and stripped.startswith("- "):
                result.append(stripped[2:])
        return result
