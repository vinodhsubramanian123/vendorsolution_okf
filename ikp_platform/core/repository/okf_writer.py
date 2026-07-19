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
                parts.append(f"{self._slugify(cat)}-rules")
            else:
                parts.append("platform-rules")
            filename = self._slugify(obj.id)
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
        # Full field dump; enums -> their .value, datetimes -> ISO strings.
        # Exclude structured lists that are handled in the Markdown body or separately.
        raw_fm: Dict[str, Any] = obj.model_dump(
            mode="json", exclude={"attributes", "relationships", "history", "evidence"}
        )

        # OKF specific required/recommended fields
        fm: Dict[str, Any] = {
            "id": obj.id,
            "type": obj.type.value,
            "title": obj.title or obj.id,
        }
        
        for k, v in raw_fm.items():
            if v is not None and v != [] and v != "":
                if k not in fm:
                    fm[k] = v

        # Ensure timestamp (last_updated defaults to now if missing)
        last_updated = getattr(obj, "last_updated", None) or datetime.now(timezone.utc)
        if isinstance(last_updated, str):
            fm["timestamp"] = last_updated if last_updated.endswith("Z") or "+" in last_updated else last_updated + "Z"
        else:
            fm["timestamp"] = last_updated.isoformat() + ("Z" if not last_updated.isoformat().endswith("Z") else "")

        # Structured attributes as frontmatter extensions
        for attr in obj.attributes:
            key = f"attr_{attr.name.lower().replace(' ', '_')}"
            fm[key] = attr.value
            if attr.unit:
                fm[f"{key}_unit"] = attr.unit
                
        # Rule specific override for version naming to match existing expectations
        if isinstance(obj, Rule) and "version" in fm:
            fm["rule_version"] = fm.pop("version")

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
