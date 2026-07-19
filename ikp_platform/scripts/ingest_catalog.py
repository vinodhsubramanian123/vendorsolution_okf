import sys
from pathlib import Path
import logging
import json
import hashlib

sys.path.append(str(Path(__file__).parent.parent.parent))

from ikp_platform.core.ingestion.pdf_extractor import PDFExtractor
from ikp_platform.core.repository.repo_manager import RepoManager
from ikp_platform.core.ontology.models import Source, SourceType

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
        if manifest.get(pdf_file.name) == checksum:
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

            # Persist objects into canonical Markdown OKF
            for obj in objects:
                repo.add_concept(obj)

            # Record the version delta
            repo._record_delta(delta)

            logger.info(f"SUCCESS: Committed {pdf_file.name} to canonical repository.")
            succeeded.append(pdf_file.name)
            manifest[pdf_file.name] = checksum

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
