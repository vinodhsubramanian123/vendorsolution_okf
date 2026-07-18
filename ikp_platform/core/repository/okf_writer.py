"""
OKF Writer — Writes engineering knowledge objects to disk in Open Knowledge Format.

Governs: OKF Spec §3–§7, Blueprint 06 §3

Responsibilities:
- Converts Pydantic models → OKF Markdown with YAML frontmatter
- Derives hierarchical directory paths from ontological position
- Generates index.md per directory (OKF §6 — progressive disclosure)
- Maintains log.md per directory (OKF §7 — change history)
- Includes full metadata in frontmatter for search-space reduction (Blueprint 06 §5)
"""

import os
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from ikp_platform.core.ontology.models import (
    BaseEngineeringObject,
    EngineeringRelationship,
    Rule,
    Constraint,
    EvidenceRecord,
)


class OKFWriter:
    """Writes engineering knowledge to disk in OKF format."""

    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)
        self.repository_path.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------
    # Path derivation — Blueprint 06 §3
    # -------------------------------------------------------------------

    def _compute_path(self, obj: BaseEngineeringObject) -> Path:
        """
        Derive hierarchical file path from the object's ontological position.

        Blueprint 06 §3:
            repository/solution-domain/product-family/generation/platform/
        """
        parts = []

        if obj.solution_domain:
            parts.append(self._slugify(obj.solution_domain))
        if obj.product_family:
            parts.append(self._slugify(obj.product_family))
        if obj.generation:
            parts.append(self._slugify(obj.generation))
        if obj.platform_id:
            parts.append(self._slugify(obj.platform_id))
        elif obj.type.value == "Platform":
            parts.append(self._slugify(obj.id))

        # Group by object type inside the hierarchy
        if obj.type.value != "Platform":
            # Pluralize type for directory name (e.g. 'rules', 'components')
            type_dir = self._slugify(obj.type.value)
            if not type_dir.endswith("s"):
                type_dir += "s"
            parts.append(type_dir)
            
            # Sub-group components by their specific category (cpu, memory, etc.)
            if obj.type.value == "Component" and hasattr(obj, "component_category") and obj.component_category:
                parts.append(self._slugify(obj.component_category))

        # Filename is the slugified id to prevent collisions across platforms
        if obj.type.value == "Rule":
            cat = getattr(obj, "component_category", None)
            if cat:
                filename = f"{self._slugify(cat)}-rules"
            else:
                filename = "platform-rules"
        else:
            filename = self._slugify(obj.id)

        return self.repository_path / Path(*parts) / f"{filename}.md"

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert a string to a filesystem-safe slug."""
        return text.lower().replace(" ", "-").replace("/", "-").replace("_", "-")

    # -------------------------------------------------------------------
    # Frontmatter generation — Blueprint 06 §5, OKF §4.1
    # -------------------------------------------------------------------

    def _generate_frontmatter(self, obj: BaseEngineeringObject) -> Dict[str, Any]:
        """
        Generate OKF-compliant YAML frontmatter with full metadata.

        OKF §4.1 Required: type
        OKF §4.1 Recommended: title, description, tags, timestamp
        Blueprint 06 §5: vendor, solution_domain, product_family, generation,
                         capabilities, lifecycle_status, etc.
        """
        fm: Dict[str, Any] = {
            "id": obj.id,
            "type": obj.type.value,
            "title": obj.title or obj.id,
        }

        # OKF recommended fields
        if obj.description:
            fm["description"] = obj.description
        if obj.tags:
            fm["tags"] = obj.tags
        fm["timestamp"] = (
            getattr(obj, "last_updated", datetime.now(timezone.utc)).isoformat() + "Z"
        )

        # Blueprint 06 §5 metadata for search-space reduction
        if obj.vendor:
            fm["vendor"] = obj.vendor
        if obj.solution_domain:
            fm["solution_domain"] = obj.solution_domain
        if obj.product_family:
            fm["product_family"] = obj.product_family
        if obj.generation:
            fm["generation"] = obj.generation
        if obj.platform_id:
            fm["platform_id"] = obj.platform_id
        if obj.lifecycle_status:
            fm["lifecycle_status"] = obj.lifecycle_status.value
        if obj.capabilities:
            fm["capabilities"] = obj.capabilities

        # Structured attributes as frontmatter extensions
        for attr in obj.attributes:
            key = f"attr_{attr.name.lower().replace(' ', '_')}"
            fm[key] = attr.value
            if attr.unit:
                fm[f"{key}_unit"] = attr.unit

        # Rule-specific fields (Blueprint 03 §8)
        if isinstance(obj, Rule):
            if obj.scope:
                fm["scope"] = obj.scope
            fm["severity"] = obj.severity.value
            fm["confidence"] = obj.confidence.value
            fm["rule_version"] = obj.version
            if obj.applicable_objects:
                fm["applicable_objects"] = obj.applicable_objects

        # Constraint-specific fields (Blueprint 03 §9)
        if isinstance(obj, Constraint):
            fm["limit_name"] = obj.limit_name
            fm["limit_value"] = obj.limit_value
            if obj.limit_unit:
                fm["limit_unit"] = obj.limit_unit

        # Component-specific fields
        if hasattr(obj, "component_category") and obj.component_category:
            fm["component_category"] = obj.component_category
        if hasattr(obj, "component_subcategory") and obj.component_subcategory:
            fm["component_subcategory"] = obj.component_subcategory

        # Platform-specific fields
        if hasattr(obj, "parent_platform_id") and obj.parent_platform_id:
            fm["parent_platform_id"] = obj.parent_platform_id
        if hasattr(obj, "platform_sku") and obj.platform_sku:
            fm["platform_sku"] = obj.platform_sku

        # SKU-specific fields
        if hasattr(obj, "part_number") and obj.part_number:
            fm["part_number"] = obj.part_number
        if hasattr(obj, "component_id") and obj.component_id:
            fm["component_id"] = obj.component_id
        if hasattr(obj, "packaging_type") and obj.packaging_type:
            fm["packaging_type"] = obj.packaging_type.value

        # Variant-specific fields
        if hasattr(obj, "base_platform_id") and obj.base_platform_id:
            fm["base_platform_id"] = obj.base_platform_id
        if hasattr(obj, "differentiators") and obj.differentiators:
            fm["differentiators"] = obj.differentiators

        # Configuration-specific fields
        if hasattr(obj, "included_components") and obj.included_components:
            fm["included_components"] = obj.included_components
        if hasattr(obj, "validated") and obj.validated:
            fm["validated"] = obj.validated

        return fm

    # -------------------------------------------------------------------
    # Body generation — OKF §4.2
    # -------------------------------------------------------------------

    def _generate_body(self, obj: BaseEngineeringObject) -> str:
        """Generate structured markdown body with capabilities, relationships, and evidence."""
        sections: List[str] = []

        # Capabilities section
        if obj.capabilities:
            lines = ["# Capabilities\n"]
            for cap in obj.capabilities:
                lines.append(f"- {cap}")
            sections.append("\n".join(lines))

        # Relationships section — uses OKF cross-links (§5)
        if obj.relationships:
            lines = ["# Relationships\n"]
            for rel in obj.relationships:
                safe_target = self._slugify(rel.target_id)
                lines.append(
                    f"- **{rel.relationship_type.value}**: "
                    f"[{rel.target_id}]({safe_target}.md)"
                )
            sections.append("\n".join(lines))

        # Rule-specific sections
        if isinstance(obj, Rule):
            if obj.trigger_conditions:
                lines = ["# Trigger Conditions\n"]
                for tc in obj.trigger_conditions:
                    lines.append(f"- {tc}")
                sections.append("\n".join(lines))
            if obj.expected_outcome:
                sections.append(f"# Expected Outcome\n\n{obj.expected_outcome}")

        # Evidence / Citations section — OKF §8
        if obj.evidence:
            lines = ["# Citations\n"]
            for i, ev in enumerate(obj.evidence, 1):
                desc = ev.description or ev.source_id
                url = ev.url or ""
                snippet = ""
                if ev.original_text_snippet:
                    snippet = f" — _{ev.original_text_snippet}_"
                if url:
                    lines.append(f"[{i}] [{desc}]({url}){snippet}")
                else:
                    lines.append(f"[{i}] {desc}{snippet}")
            sections.append("\n".join(lines))

        return "\n\n".join(sections)

    # -------------------------------------------------------------------
    # Write concept — main entry point
    # -------------------------------------------------------------------

    def write_concept(self, obj: BaseEngineeringObject) -> str:
        """
        Writes a single engineering concept to disk as an OKF Markdown file.
        Returns the path relative to the repository root.
        """
        frontmatter = self._generate_frontmatter(obj)
        body = self._generate_body(obj)

        file_path = self._compute_path(obj)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        import re
        
        block = "---\n"
        block += yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        block += "---\n\n"
        if body:
            block += body + "\n"

        if obj.type.value == "Rule":
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                # Look for existing block with the same id to replace it
                pattern_str = r"^---\n.*?\nid:\s*['\"]?" + re.escape(obj.id) + r"['\"]?\n.*?\n---\n.*?(?=\n---|$)"
                pattern = re.compile(pattern_str, re.MULTILINE | re.DOTALL)
                
                if pattern.search(content):
                    content = pattern.sub(block.strip(), content, count=1)
                else:
                    content = content.strip() + "\n\n" + block.strip()
                    
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content.strip() + "\n")
            else:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(block)
        else:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(block)

        return str(file_path.relative_to(self.repository_path))

    # -------------------------------------------------------------------
    # Index generation — OKF §6
    # -------------------------------------------------------------------

    def generate_index(self, directory: Optional[Path] = None) -> str:
        """
        Generate an index.md for the given directory listing all .md concepts.
        OKF §6: Supports progressive disclosure.
        """
        target_dir = directory or self.repository_path
        target_dir = Path(target_dir)

        entries_by_section: Dict[str, List[str]] = {}

        for item in sorted(target_dir.iterdir()):
            if item.name in ("index.md", "log.md"):
                continue

            if item.is_dir():
                section = "Subdirectories"
                sub_index = item / "index.md"
                desc = ""
                if sub_index.exists():
                    # Try to extract first description from sub-index
                    desc = f" - {item.name} knowledge"
                entries_by_section.setdefault(section, []).append(
                    f"* [{item.name}]({item.name}/) {desc}"
                )
            elif item.suffix == ".md":
                # Parse frontmatter to extract type and description
                fm = self._read_frontmatter(item)
                obj_type = fm.get("type", "Concept")
                title = fm.get("title", item.stem)
                desc = fm.get("description", "")
                section = obj_type
                entry = f"* [{title}]({item.name})"
                if desc:
                    entry += f" - {desc}"
                entries_by_section.setdefault(section, []).append(entry)

        # Build index content
        lines = []
        for section, entries in entries_by_section.items():
            lines.append(f"# {section}\n")
            lines.extend(entries)
            lines.append("")

        index_path = target_dir / "index.md"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return str(index_path.relative_to(self.repository_path))

    # -------------------------------------------------------------------
    # Log maintenance — OKF §7
    # -------------------------------------------------------------------

    def append_log_entry(
        self,
        action: str,
        description: str,
        concept_path: Optional[str] = None,
        directory: Optional[Path] = None,
    ) -> None:
        """
        Append an entry to log.md in OKF §7 format.
        Date headings use ISO 8601 YYYY-MM-DD.
        """
        target_dir = directory or self.repository_path
        log_path = Path(target_dir) / "log.md"

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        link_text = ""
        if concept_path:
            link_text = f" for [{concept_path}]({concept_path})"

        entry = f"* **{action}**: {description}{link_text}.\n"

        # Read existing content
        existing = ""
        if log_path.exists():
            with open(log_path, "r", encoding="utf-8") as f:
                existing = f.read()

        # Check if today's date heading already exists
        date_heading = f"## {today}"
        if date_heading in existing:
            # Insert entry after the date heading
            parts = existing.split(date_heading, 1)
            updated = parts[0] + date_heading + "\n" + entry + parts[1]
        else:
            # Add new date heading at top (after title if present)
            if existing.startswith("# "):
                # Preserve title line
                title_end = existing.index("\n") + 1
                updated = (
                    existing[:title_end]
                    + f"\n{date_heading}\n{entry}\n"
                    + existing[title_end:]
                )
            else:
                updated = f"# Repository Update Log\n\n{date_heading}\n{entry}\n" + existing

        with open(log_path, "w", encoding="utf-8") as f:
            f.write(updated)

    # -------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------

    @staticmethod
    def _read_frontmatter(file_path: Path) -> Dict[str, Any]:
        """Read YAML frontmatter from an OKF Markdown file."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("---"):
            return {}

        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}

        try:
            return yaml.safe_load(parts[1]) or {}
        except yaml.YAMLError:
            return {}
