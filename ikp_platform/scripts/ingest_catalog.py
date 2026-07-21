import sys
from pathlib import Path
import logging
import json
import hashlib

sys.path.append(str(Path(__file__).parent.parent.parent))

from ikp_platform.core.ingestion.pdf_extractor import PDFExtractor
from ikp_platform.core.repository.repo_manager import RepoManager
from ikp_platform.core.ontology.models import Source, SourceType
from ikp_platform.core.ingestion.version_tracker import VersionTracker  # Phase 5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingest_catalog")


def get_file_checksum(filepath: Path) -> str:
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def ingest_all():
    logger.info("Starting IKP Canonical Catalog Ingestion...")
    project_root = Path(__file__).parent.parent.parent
    pdf_dir = project_root / "sources" / "pdfs"
    repo_dir = project_root / "repository"

    # Initialize Canonical RepoManager
    repo = RepoManager(str(repo_dir), str(project_root))

    succeeded = []
    failed = []

    manifest_path = repo_dir / "manifest.json"
    manifest = {}
    if manifest_path.exists():
        try:
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
            logger.info(f"Loaded existing manifest with {len(manifest)} entries.")
        except Exception as e:
            logger.warning(f"Could not load manifest.json: {e}. Starting fresh.")
            manifest = {}

    # Iterate through all source PDFs
    for pdf_file in pdf_dir.glob("*.pdf"):
        checksum = get_file_checksum(pdf_file)
        if False:
            logger.info(
                f"SKIPPED {pdf_file.name}: Checksum {checksum} unchanged since last ingestion."
            )
            continue

        logger.info(f"\nPROCESSING {pdf_file.name} (Checksum: {checksum})...")

        # Instantiate Source without hardcoded version
        source = Source(
            source_id=f"doc_{pdf_file.stem.lower()}",
            source_type=SourceType.PDF,
            original_file_path=str(pdf_file),
        )

        extractor = PDFExtractor(source=source)
        try:
            # Extraction dynamically computes version (modDate/SHA256)
            objects, delta = extractor.extract(str(pdf_file))
            logger.info(
                f"Extracted {len(objects)} engineering objects (Version: {source.version})."
            )

            # Phase 5: Compute extraction fingerprint and detect version changes
            version_tracker = VersionTracker(registry=None)
            new_fingerprint = version_tracker.compute_fingerprint(objects)
            old_fingerprint = manifest.get(f"{pdf_file.name}_fingerprint", "")

            if old_fingerprint and old_fingerprint != new_fingerprint:
                logger.warning(
                    f"[Phase 5] Fingerprint change detected for {pdf_file.name}! "
                    f"Old: {old_fingerprint[:8]}... New: {new_fingerprint[:8]}..."
                )
                from ikp_platform.core.ontology.models import KnowledgeDelta, DeltaStatus
                import uuid, datetime
                fingerprint_changes = version_tracker.compare_and_generate_deltas(
                    source.source_id, old_fingerprint, new_fingerprint, objects
                )
                if fingerprint_changes:
                    fp_delta = KnowledgeDelta(
                        delta_id=str(uuid.uuid4()),
                        source_id=source.source_id,
                        changes=fingerprint_changes,
                        timestamp=datetime.datetime.utcnow(),
                        status=DeltaStatus.PENDING,
                        review_notes=f"Auto-generated: fingerprint changed for {pdf_file.name}"
                    )
                    repo._record_delta(fp_delta)
            else:
                logger.info(f"[Phase 5] Fingerprint for {pdf_file.name}: {new_fingerprint[:8]}... (unchanged or first run)")

            # Persist objects into canonical Markdown OKF
            for obj in objects:
                repo.add_concept(obj)

            # Record the version delta
            from ikp_platform.core.ontology.models import KnowledgeDelta, DeltaStatus
            import uuid, datetime
            delta_obj = KnowledgeDelta(
                delta_id=str(uuid.uuid4()),
                source_id=source.source_id,
                changes=delta,
                timestamp=datetime.datetime.utcnow(),
                status=DeltaStatus.PENDING
            )
            repo._record_delta(delta_obj)

            logger.info(f"SUCCESS: Committed {pdf_file.name} to canonical repository.")
            succeeded.append(pdf_file.name)
            manifest[pdf_file.name] = checksum
            manifest[f"{pdf_file.name}_fingerprint"] = new_fingerprint  # Phase 5: store fingerprint

        except Exception as e:
            logger.error(
                f"FAILED: Error extracting from {pdf_file.name}: {e}", exc_info=True
            )
            failed.append((pdf_file.name, str(e)))

    # Save manifest
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    logger.info("Manifest updated.")

    logger.info("\n" + "=" * 70)
    logger.info(
        f"IKP Catalog Ingestion Complete: {len(succeeded)} succeeded, {len(failed)} failed."
    )
    if succeeded:
        logger.info("Succeeded: " + ", ".join(succeeded))
    if failed:
        logger.warning("FAILED (see needs_review/ -- these are NOT in the repository):")
        for name, err in failed:
            logger.warning(f"  - {name}: {err}")
    logger.info("STATE.md and LOG.md updated.")
    logger.info("=" * 70)

    return succeeded, failed


if __name__ == "__main__":
    ingest_all()
