"""
Repository Manager — Orchestrates bidirectional sync between OKF files and the in-memory graph.

Governs: Blueprint 06 (Canonical Repository), Blueprint 02 §4 (Repository Responsibilities)

Responsibilities:
- On startup: OKF Reader → Graph Builder (bootstrap)
- On change: Graph Builder + OKF Writer (persist)
- Updates CONTEXT.md, STATE.md, LOG.md
"""

from pathlib import Path
from datetime import datetime, timezone
from typing import List
import difflib

from ikp_platform.core.ontology.models import (
    BaseEngineeringObject,
    KnowledgeDelta,
    DeltaStatus,
)
from ikp_platform.core.repository.okf_reader import OKFReader
from ikp_platform.core.repository.okf_writer import OKFWriter
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.repository.vector_store import VectorStore
from ikp_platform.core.repository.mcp_client import ObsidianMCPClient


class RepoManager:
    """
    Central orchestrator for the dual-layer architecture.

    - Persistence layer: OKF Markdown files on disk
    - Active layer: NetworkX DiGraph in memory
    """

    def __init__(self, repository_path: str, project_root: str):
        self.repository_path = Path(repository_path)
        self.project_root = Path(project_root)
        self.reader = OKFReader(repository_path)
        self.writer = OKFWriter(repository_path)
        self.graph = GraphBuilder()

        # Initialize Vector Store
        vector_db_path = self.project_root / ".chroma"
        vector_db_path.mkdir(exist_ok=True)
        self.vector_store = VectorStore(str(vector_db_path))

        # Initialize MCP Client
        self.mcp_client = ObsidianMCPClient(str(self.repository_path))

    # -------------------------------------------------------------------
    # Bootstrap — load existing repository into graph
    # -------------------------------------------------------------------

    def bootstrap(self) -> int:
        """
        Load all existing OKF files into the in-memory graph.
        Returns the number of concepts loaded.
        """
        objects = self.reader.load_all()
        for obj in objects:
            self.graph.add_concept(obj)

        self._update_state_file()
        return len(objects)

    # -------------------------------------------------------------------
    # Add / update concepts
    # -------------------------------------------------------------------

    def add_concept(self, obj: BaseEngineeringObject) -> str:
        """
        Add a new engineering concept to both layers.
        Returns the relative path of the written OKF file.

        NOTE: this deliberately does NOT touch the vector store. Ingestion
        (this method) should only ever require local disk I/O; embedding
        generation requires a live LLM API call per object and was
        previously invoked here synchronously -- meaning ingesting the
        whole catalog required 100+ blocking network round-trips and
        failed silently (falling back to empty results) whenever no API
        key was configured. Call `reindex_vector_store()` as a separate,
        explicit step (see scripts/reindex.py) once ingestion is done.
        """
        # Deduplication Check
        # Perform local semantic text similarity (difflib) to prevent duplicates without LLM I/O
        if obj.type.value == "Rule" and obj.platform_id:
            for existing_id, data in self.graph.graph.nodes(data=True):
                if (
                    data.get("type") == "Rule"
                    and data.get("platform_id") == obj.platform_id
                ):
                    existing_desc = data.get("description", "")
                    if (
                        existing_desc
                        and difflib.SequenceMatcher(
                            None, obj.description or "", existing_desc
                        ).ratio()
                        > 0.90
                    ):
                        # Semantic duplicate found. Align IDs to merge them.
                        obj.id = existing_id
                        break

        if obj.id in self.graph.graph:
            # We already have this concept. We could merge, but for now we just skip duplicating it in LOG.md
            # We still overwrite the OKF file to allow updates.
            is_new = False
            # Merge evidence if it's an update
            existing_node = self.graph.graph.nodes[obj.id]
            if "evidence" in existing_node:
                existing_ev = existing_node["evidence"]
                # Only append if source_id is different
                for ev in obj.evidence:
                    if not any(e.get("source_id") == ev.source_id for e in existing_ev):
                        existing_ev.append(ev.model_dump())
                # Update the object's evidence list before writing
                from ikp_platform.core.ontology.models import EvidenceRecord

                obj.evidence = [EvidenceRecord(**e) for e in existing_ev]
        else:
            is_new = True

        # Persist to OKF Markdown
        existing_path = getattr(obj, "source_filepath", None) or self.reader.path_cache.get(obj.id)
        if existing_path and Path(existing_path).is_absolute():
            try:
                existing_path = str(Path(existing_path).relative_to(self.repository_path))
            except ValueError:
                pass
        relative_path = self.writer.write_concept(obj, existing_path=existing_path)
        self.reader.path_cache[obj.id] = relative_path

        # Add to in-memory graph
        self.graph.add_concept(obj)

        action = "Creation" if is_new else "Update"
        description = f"{'Added' if is_new else 'Updated'} {obj.type.value}: {obj.title or obj.id}"

        # Update log (both creations and updates -- previously only
        # creations were logged, so re-ingesting a changed source
        # document left no audit trail of what changed).
        self.writer.append_log_entry(
            action=action,
            description=description,
            concept_path=relative_path,
        )
        self._update_state_file()
        self._append_root_log(description)

        # Regenerate index for parent directory
        file_path = self.repository_path / relative_path
        self.writer.generate_index(file_path.parent)

        return relative_path

    def reindex_vector_store(self, batch_size: int = 20) -> int:
        """
        (Re)build the semantic search index from everything currently on
        disk in repository/. Separate from add_concept() on purpose --
        see its docstring. Batches embedding calls instead of one API
        call per object. Returns the number of objects indexed.
        """
        objects = self.reader.load_all()
        return self.vector_store.index_many(objects, batch_size=batch_size)

    def apply_delta(
        self, delta: KnowledgeDelta, objects: List[BaseEngineeringObject]
    ) -> None:
        """
        Apply a validated Knowledge Delta — persist all objects and record the delta.

        Blueprint 02 §7: Knowledge Deltas SHALL be merged into canonical
        knowledge while preserving history.
        """
        for obj in objects:
            self.add_concept(obj)

        # Record the delta in history/
        self._record_delta(delta)

        delta.status = DeltaStatus.MERGED

    # -------------------------------------------------------------------
    # Managed files — Blueprint 02 §4
    # -------------------------------------------------------------------

    def _update_state_file(self) -> None:
        """Update STATE.md with current platform statistics."""
        stats = self.graph.get_stats()
        state_path = self.project_root / "STATE.md"

        lines = [
            "# IKP Platform State\n",
            f"**Last Updated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n",
            "## Knowledge Graph Statistics\n",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Total Nodes | {stats['total_nodes']} |",
            f"| Total Edges | {stats['total_edges']} |",
        ]

        type_counts = stats.get("type_counts", {})
        if isinstance(type_counts, dict) and type_counts:
            lines.append("\n## Objects by Type\n")
            lines.append("| Type | Count |")
            lines.append("|------|-------|")
            for obj_type, count in sorted(type_counts.items()):
                lines.append(f"| {obj_type} | {count} |")

        with open(state_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    def _append_root_log(self, description: str) -> None:
        """Append an entry to the project root LOG.md."""
        log_path = self.project_root / "LOG.md"
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        time_str = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

        entry = f"* `{time_str}` — {description}\n"

        existing = ""
        if log_path.exists():
            with open(log_path, "r", encoding="utf-8") as f:
                existing = f.read()

        date_heading = f"## {today}"
        if date_heading in existing:
            parts = existing.split(date_heading, 1)
            updated = parts[0] + date_heading + "\n" + entry + parts[1]
        else:
            if existing.startswith("# "):
                title_end = existing.index("\n") + 1
                updated = (
                    existing[:title_end]
                    + f"\n{date_heading}\n{entry}\n"
                    + existing[title_end:]
                )
            else:
                updated = f"# IKP Operations Log\n\n{date_heading}\n{entry}\n"

        with open(log_path, "w", encoding="utf-8") as f:
            f.write(updated)

    def _record_delta(self, delta: KnowledgeDelta) -> None:
        """Record a Knowledge Delta in the history/ directory."""
        history_dir = self.project_root / "history"
        history_dir.mkdir(exist_ok=True)

        date_str = delta.timestamp.strftime("%Y-%m-%d")
        filename = f"{date_str}_{delta.delta_id}.md"
        delta_path = history_dir / filename

        lines = [
            "---",
            "type: Knowledge Delta",
            f"title: {delta.delta_id}",
            f"description: Delta from source {delta.source_id}",
            f"timestamp: {delta.timestamp.isoformat()}Z",
            f"tags: [delta, {delta.status.value.lower()}]",
            "---\n",
            f"# Knowledge Delta: {delta.delta_id}\n",
            f"**Source**: {delta.source_id}",
            f"**Status**: {delta.status.value}",
            f"**Changes**: {len(delta.changes)}\n",
        ]

        if delta.changes:
            lines.append("## Changes\n")
            lines.append("| Type | Object | Field | New Value |")
            lines.append("|------|--------|-------|-----------|")
            for change in delta.changes:
                lines.append(
                    f"| {change.change_type.value} | {change.object_id} | "
                    f"{change.field_name or '-'} | {change.new_value or '-'} |"
                )

        if delta.review_notes:
            lines.append(f"\n## Review Notes\n\n{delta.review_notes}")

        with open(delta_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    def update_context(self, domains: List[str], source_count: int) -> None:
        """Update CONTEXT.md with current engineering coverage."""
        context_path = self.project_root / "CONTEXT.md"

        lines = [
            "# IKP Engineering Context\n",
            f"**Last Updated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n",
            "## Coverage\n",
        ]

        if domains:
            lines.append("### Solution Domains\n")
            for domain in domains:
                lines.append(f"- {domain}")
            lines.append("")

        lines.append(f"### Sources Ingested: {source_count}\n")

        with open(context_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
