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
import logging

import logging
logger = logging.getLogger("ikp.repository.reader")

from ikp_platform.core.ontology.models import (
    BaseEngineeringObject,
    EngineeringObjectType,
    EngineeringRelationship,
    RelationshipType,
    EngineeringAttribute,
    EvidenceRecord,
    LifecycleStatus,
    Rule,
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
)


class OKFReader:
    """Parses OKF Markdown files and reconstructs Pydantic engineering objects."""

    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)
        self.path_cache: Dict[str, str] = {}

    def load_all(self) -> List[BaseEngineeringObject]:
        """
        Recursively scan the repository and parse all concept files.
        Skips reserved files (index.md, log.md).
        """
        objects: List[BaseEngineeringObject] = []
        if not self.repository_path.exists():
            return objects

        for md_file in sorted(self.repository_path.rglob("*.md")):
            if md_file.name in ("index.md", "log.md"):
                continue
            objs = self._parse_file(md_file)
            if objs:
                objects.extend(objs)

        return objects

    def _parse_file(self, file_path: Path) -> List[BaseEngineeringObject]:
        """Parse an OKF Markdown file that may contain multiple Pydantic models."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        objects = []
        # Split by document separators if multiple exist
        # A valid OKF block is:
        # ---
        # yaml...
        # ---
        # body
        #
        # If there are multiple, they will look like:
        # ---
        # yaml1
        # ---
        # body1
        # ---
        # yaml2
        # ---
        # body2

        # We can split by "\n---\n" and handle chunks.
        import re

        # Find all frontmatter blocks
        pattern = re.compile(r"(?:^|\n)---\n(.*?)\n---\n(.*?)(?=\n---\n|\Z)", re.DOTALL)

        matches = pattern.findall(content)
        if not matches:
            # Fallback to single block parser if regex misses
            fm, body = self._split_frontmatter(content)
            if fm:
                obj = self._build_object(fm, body, file_path)
                if obj:
                    objects.append(obj)
            return objects

        for yaml_content, body_content in matches:
            try:
                fm = yaml.safe_load(yaml_content) or {}
                if fm:
                    obj = self._build_object(fm, body_content.strip(), file_path)
                    if obj:
                        objects.append(obj)
            except yaml.YAMLError:
                continue

        return objects

    def _build_object(
        self, frontmatter: Dict[str, Any], body: str, file_path: Path
    ) -> Optional[BaseEngineeringObject]:
        """Helper to build a Pydantic object from frontmatter and body."""

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
            attributes.append(
                EngineeringAttribute(
                    name=attr_name,
                    value=frontmatter[key],
                    unit=frontmatter.get(unit_key),
                )
            )

        # Parse lifecycle status
        lifecycle_str = frontmatter.get("lifecycle_status", "Unknown")
        try:
            lifecycle = LifecycleStatus(lifecycle_str)
        except ValueError:
            lifecycle = LifecycleStatus.UNKNOWN

        # Parse timestamp
        timestamp = datetime.now(timezone.utc)
        ts = frontmatter.get("timestamp")
        if ts:
            try:
                if isinstance(ts, datetime):
                    timestamp = ts
                else:
                    timestamp = datetime.fromisoformat(ts.rstrip("Z"))
            except (ValueError, AttributeError):
                pass

        # Derive ID from frontmatter if available, otherwise fallback to file path
        relative = file_path.relative_to(self.repository_path)
        obj_id = frontmatter.get("id", str(relative.with_suffix("")))
        self.path_cache[obj_id] = str(relative)

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
            "timestamp": timestamp,
            "attributes": attributes,
            "relationships": relationships,
            "capabilities": frontmatter.get("capabilities", []),
            "tags": frontmatter.get("tags", []),
            "aliases": frontmatter.get("aliases", []),
            "evidence": evidence,
        }

        # Merge all data into a single dict for Pydantic validation
        merged_data = {**frontmatter, **kwargs}
        merged_data["source_filepath"] = str(file_path.absolute())

        TYPE_MAP = {
            EngineeringObjectType.RULE: Rule,
            EngineeringObjectType.CONSTRAINT: Constraint,
            EngineeringObjectType.COMPONENT: Component,
            EngineeringObjectType.PLATFORM: Platform,
            EngineeringObjectType.SKU: SKU,
            EngineeringObjectType.WORKLOAD: Workload,
            EngineeringObjectType.CATEGORY_LIMIT: CategoryLimit,
            EngineeringObjectType.SLOT_MAPPING: SlotMapping,
            EngineeringObjectType.SOLUTION_CATEGORY: SolutionCategory,
            EngineeringObjectType.VARIANT: Variant,
            EngineeringObjectType.CONFIGURATION: Configuration,
        }
        
        ModelClass = TYPE_MAP.get(obj_type, BaseEngineeringObject)

        # Inject body-extracted rule specifics
        if obj_type == EngineeringObjectType.RULE:
            extracted_outcome = self._extract_section(body, "Expected Outcome")
            extracted_triggers = self._extract_list_section(body, "Trigger Conditions")
            if extracted_outcome:
                merged_data["expected_outcome"] = extracted_outcome
            if extracted_triggers:
                merged_data["trigger_conditions"] = extracted_triggers

        try:
            return getattr(ModelClass, "model_validate")(merged_data)
        except Exception as e:
            logger.error(f"Failed to fully validate {obj_id} as {ModelClass.__name__}, falling back to base object: {e}")
            try:
                return BaseEngineeringObject.model_validate(merged_data)
            except Exception as base_e:
                logger.error(f"Absolute validation failure for {obj_id}: {base_e}")
                return None

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

                    relationships.append(
                        EngineeringRelationship(
                            target_id=target_id,
                            relationship_type=rel_type,
                        )
                    )
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
                    rest = stripped[bracket_end + 1 :].strip()

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

                    evidence.append(
                        EvidenceRecord(
                            source_id=desc,
                            description=desc,
                            url=url,
                            original_text_snippet=snippet,
                        )
                    )
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
