import sys
from pathlib import Path
import logging

sys.path.append(str(Path(__file__).parent.parent.parent))

from ikp_platform.core.ingestion.pdf_extractor import PDFExtractor
from ikp_platform.core.repository.repo_manager import RepoManager
from ikp_platform.core.ontology.models import Source, SourceType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingest_catalog")

def ingest_all():
    logger.info("Starting IKP Canonical Catalog Ingestion...")
    project_root = Path(__file__).parent.parent.parent
    pdf_dir = project_root / "sources" / "pdfs"
    repo_dir = project_root / "repository"
    
    # Initialize Canonical RepoManager
    repo = RepoManager(str(repo_dir), str(project_root))

    succeeded = []
    failed = []
    
    # Iterate through all source PDFs
    for pdf_file in pdf_dir.glob("*.pdf"):
        logger.info(f"\nProcessing {pdf_file.name}...")
        
        # Instantiate Source without hardcoded version
        source = Source(
            source_id=f"doc_{pdf_file.stem.lower()}",
            source_type=SourceType.PDF,
            original_file_path=str(pdf_file)
        )
        
        extractor = PDFExtractor(source=source)
        try:
            # Extraction dynamically computes version (modDate/SHA256)
            objects, delta = extractor.extract(str(pdf_file))
            logger.info(f"Extracted {len(objects)} engineering objects (Version: {source.version}).")
            
            # Persist objects into canonical Markdown OKF
            for obj in objects:
                repo.add_concept(obj)
            
            # Record the version delta
            repo._record_delta(delta)
            
            logger.info(f"Successfully committed {pdf_file.name} to canonical repository.")
            succeeded.append(pdf_file.name)

        except Exception as e:
            logger.error(f"Error extracting from {pdf_file.name}: {e}", exc_info=True)
            failed.append((pdf_file.name, str(e)))

    logger.info("\n" + "=" * 70)
    logger.info(f"IKP Catalog Ingestion Complete: {len(succeeded)} succeeded, {len(failed)} failed.")
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
