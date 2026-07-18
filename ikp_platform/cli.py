"""
IKP CLI — Command-line interface for the Infrastructure Knowledge Platform.

Usage:
    python -m ikp_platform.cli ingest <path> [--platform-id=<id>]
                                                  Ingest an engineering source.
                                                  --platform-id links Excel/BOQ
                                                  components to a platform via
                                                  COMPATIBLE_WITH (required for
                                                  them to be reachable by
                                                  solution generation).
    python -m ikp_platform.cli query "<text>"    Query the knowledge base
    python -m ikp_platform.cli validate <id>      Validate a solution candidate
    python -m ikp_platform.cli learn              Run the continuous learning loop
    python -m ikp_platform.cli mcp                Start the MCP stdio server
    python -m ikp_platform.cli status             Show platform state
    python -m ikp_platform.cli scan               Scan sources/ for new files
"""

import sys
import os
import logging
from pathlib import Path

from ikp_platform.utils.logger import setup_logger

# Setup logging
logger = setup_logger("ikp")

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
REPOSITORY_PATH = PROJECT_ROOT / "repository"
SOURCES_PATH = PROJECT_ROOT / "sources"

from ikp_platform.core.repository.repo_manager import RepoManager
from ikp_platform.core.ingestion.source_registry import SourceRegistry
from ikp_platform.core.ingestion.source_watcher import SourceWatcher
from ikp_platform.core.ingestion.pdf_extractor import PDFExtractor
from ikp_platform.core.ingestion.excel_parser import ExcelExtractor
from ikp_platform.core.ontology.models import ProcessingStatus, SourceType
from ikp_platform.core.reasoning.intent_parser import IntentParser
from ikp_platform.core.reasoning.solution_generator import SolutionGenerator


def cmd_ingest(file_path: str, platform_id: str = None):
    """Ingest a single engineering source file."""
    logger.info(f"=== IKP Ingestion Pipeline ===")
    logger.info(f"Source: {file_path}")

    # 1. Initialize repository manager
    repo = RepoManager(str(REPOSITORY_PATH), str(PROJECT_ROOT))
    count = repo.bootstrap()
    logger.info(f"Bootstrapped repository: {count} existing objects")

    # 2. Register source
    registry = SourceRegistry()
    source = registry.register(file_path)
    logger.info(f"Registered: {source.source_id} ({source.source_type.value})")

    # 3. Extract based on source type
    if source.source_type == SourceType.PDF:
        registry.update_status(source.source_id, ProcessingStatus.EXTRACTING)

        extractor = PDFExtractor(source)
        objects, delta = extractor.extract(file_path)

        logger.info(f"Extracted {len(objects)} engineering objects")
        logger.info(f"Knowledge Delta: {delta.delta_id} with {len(delta.changes)} changes")

        # 4. Persist to dual-layer repository
        registry.update_status(source.source_id, ProcessingStatus.NORMALIZING)

        for obj in objects:
            path = repo.add_concept(obj)
            logger.info(f"  Written: {path}")

        # 5. Record delta
        repo._record_delta(delta)

        # 6. Update context
        domains = list(set(
            obj.solution_domain for obj in objects
            if obj.solution_domain
        ))
        repo.update_context(domains, len(registry.sources))

        registry.update_status(source.source_id, ProcessingStatus.COMPLETED)

        # 7. Print summary
        stats = repo.graph.get_stats()
        logger.info(f"=== Ingestion Complete ===")
        logger.info(f"Total nodes in graph: {stats['total_nodes']}")
        logger.info(f"Total edges in graph: {stats['total_edges']}")
        logger.info(f"Objects by type:")
        for obj_type, count in sorted(stats.get('type_counts', {}).items()):
            logger.info(f"  {obj_type}: {count}")
    elif source.source_type == SourceType.EXCEL:
        registry.update_status(source.source_id, ProcessingStatus.EXTRACTING)

        extractor = ExcelExtractor()
        objects, delta = extractor.extract(source, file_path, platform_id=platform_id)

        logger.info(f"Extracted {len(objects)} engineering objects")
        logger.info(f"Knowledge Delta: {delta.delta_id} with {len(delta.changes)} changes")

        registry.update_status(source.source_id, ProcessingStatus.NORMALIZING)

        for obj in objects:
            path = repo.add_concept(obj)
            logger.info(f"  Written: {path}")

        repo._record_delta(delta)

        domains = list(set(
            obj.solution_domain for obj in objects
            if obj.solution_domain
        ))
        repo.update_context(domains, len(registry.sources))

        registry.update_status(source.source_id, ProcessingStatus.COMPLETED)

        stats = repo.graph.get_stats()
        logger.info(f"=== Ingestion Complete ===")
        logger.info(f"Total nodes in graph: {stats['total_nodes']}")
        logger.info(f"Total edges in graph: {stats['total_edges']}")
    else:
        logger.warning(f"Source type {source.source_type.value} not yet supported")


def cmd_status():
    """Show current platform state."""
    repo = RepoManager(str(REPOSITORY_PATH), str(PROJECT_ROOT))
    count = repo.bootstrap()

    stats = repo.graph.get_stats()
    print(f"\n{'='*50}")
    print(f"  IKP Platform Status")
    print(f"{'='*50}")
    print(f"  Repository objects: {stats['total_nodes']}")
    print(f"  Relationships:      {stats['total_edges']}")
    print()

    type_counts = stats.get('type_counts', {})
    if type_counts:
        print(f"  Objects by type:")
        for obj_type, count in sorted(type_counts.items()):
            print(f"    {obj_type}: {count}")
    print(f"{'='*50}\n")


def cmd_scan():
    """Scan sources/ directory for new files and ingest them."""
    watcher = SourceWatcher(str(SOURCES_PATH))
    new_files = watcher.scan()

    if not new_files:
        logger.info("No new source files found")
        return

    logger.info(f"Found {len(new_files)} new source file(s)")
    success = 0
    failed = 0
    for f in new_files:
        try:
            cmd_ingest(f)
            success += 1
        except Exception as e:
            logger.error(f"Failed to ingest {f}: {e}")
            failed += 1
    logger.info(f"Scan complete: {success} succeeded, {failed} failed out of {len(new_files)} files")


def cmd_query(query_text: str):
    """Query the knowledge base with natural language."""
    logger.info(f"=== IKP Query ===")
    logger.info(f"Query: {query_text}")
    
    # Bootstrap repository
    repo = RepoManager(str(REPOSITORY_PATH), str(PROJECT_ROOT))
    repo.bootstrap()
    
    # Parse intent
    parser = IntentParser()
    request = parser.parse_request(query_text)
    
    # Generate solutions
    generator = SolutionGenerator(repo.graph, repo.vector_store, repo.mcp_client)
    candidates = generator.generate(request)
    
    if not candidates:
        logger.warning("No valid solutions found for the request.")
        return
        
    logger.info(f"Found {len(candidates)} solution candidates:")
    for i, candidate in enumerate(candidates, 1):
        print(f"\n--- Candidate {i} [{candidate.profile}] ---")
        print(f"Status: {candidate.validation_status}")
        print(f"Confidence: {candidate.confidence.value}")
        print("Components:")
        for comp in candidate.components:
            print(f"  - {comp}")
        print("Reasoning Chain:")
        for step in candidate.reasoning_chain:
            print(f"  > {step}")
    print()


def cmd_validate(solution_id: str):
    """Validate a solution candidate against engineering rules/vendor systems."""
    logger.info(f"=== IKP Vendor Validation ===")
    logger.info(f"Validating Solution: {solution_id}")
    
    from ikp_platform.core.validation.validator import ManualReviewValidator
    validator = ManualReviewValidator()
    
    # In V1.0, this generates a manual review request delta
    result = validator.validate([], {"solution_id": solution_id})
    logger.info(f"Validation Result: Valid={result.is_valid}")
    for msg in result.messages:
        logger.info(f"[{msg.severity}] {msg.message}")
        
    delta = validator.to_knowledge_delta(result)
    
    repo = RepoManager(str(REPOSITORY_PATH), str(PROJECT_ROOT))
    repo._record_delta(delta)
    logger.info(f"Recorded Knowledge Delta: {delta.delta_id} in history/")


def cmd_learn():
    """Run the continuous learning loop to process pending knowledge deltas."""
    logger.info(f"=== IKP Learning Loop ===")
    history_dir = PROJECT_ROOT / "history"
    if not history_dir.exists():
        logger.info("No pending deltas in history/")
        return
        
    count = 0
    for file in history_dir.glob("*.md"):
        count += 1
        
    logger.info(f"Found {count} delta records in history/")
    logger.info("Manual review required for V1.0 deltas before merging into canonical knowledge.")


def cmd_mcp():
    """Start the MCP server over stdio."""
    # We must run it as a subprocess or import and run asyncio
    import subprocess
    logger.info("Starting IKP MCP Server...")
    server_script = PROJECT_ROOT / "ikp_platform" / "mcp_server.py"
    subprocess.run([sys.executable, str(server_script)])


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "ingest" and len(sys.argv) >= 3:
        platform_id = None
        for arg in sys.argv[3:]:
            if arg.startswith("--platform-id="):
                platform_id = arg.split("=", 1)[1]
        cmd_ingest(sys.argv[2], platform_id=platform_id)
    elif command == "query" and len(sys.argv) >= 3:
        cmd_query(sys.argv[2])
    elif command == "validate" and len(sys.argv) >= 3:
        cmd_validate(sys.argv[2])
    elif command == "learn":
        cmd_learn()
    elif command == "mcp":
        cmd_mcp()
    elif command == "status":
        cmd_status()
    elif command == "scan":
        cmd_scan()
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
