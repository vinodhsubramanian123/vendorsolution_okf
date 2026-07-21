import chromadb
import logging
import time
from typing import List, Dict, Any, Optional, Tuple
from ikp_platform.core.ontology.models import BaseEngineeringObject
from ikp_platform.core.reasoning.llm_client import LLMClient

logger = logging.getLogger("ikp.repository.vector")


class VectorStore:
    def __init__(self, persist_directory: str):
        self.persist_directory = persist_directory
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="ikp_components")
        self.llm = LLMClient()

    def index_object(self, obj: BaseEngineeringObject) -> int:
        """Vectorize and index a single object."""
        return self.index_many([obj])

    def index_many(
        self, objects: List[BaseEngineeringObject], batch_size: int = 20
    ) -> int:
        """Vectorize and index a list of objects.

        NOTE: The Gemini embed_content API only returns a single embedding
        when given a list — it does NOT batch. We therefore embed one object
        at a time and upsert in batches to keep ChromaDB round-trips low.
        Returns the number of objects successfully indexed.
        """
        indexable = [
            o
            for o in objects
            if o is not None
            and o.type.value
            in ["Platform", "Component", "SKU", "Rule", "SolutionCategory"]
        ]
        if not indexable:
            return 0

        indexed_count = 0
        ids_batch: List[str] = []
        docs_batch: List[str] = []
        metas_batch: List[Dict[str, Any]] = []
        embs_batch: List[List[float]] = []

        for obj in indexable:
            text_repr = self._text_repr(obj)

            # Embed one at a time — the API ignores extra list items
            embedding = None
            for attempt in range(3):
                try:
                    embs = self.llm.generate_embeddings([text_repr])
                    if embs and not all(v == 0.0 for v in embs[0]):
                        embedding = embs[0]
                        break
                    # Zero embedding = API failure, retry after backoff
                    if attempt < 2:
                        time.sleep(1.0 * (attempt + 1))
                except Exception as e:
                    logger.warning(f"Embedding attempt {attempt+1} failed for {obj.id}: {e}")
                    if attempt < 2:
                        time.sleep(1.0 * (attempt + 1))

            if embedding is None:
                logger.warning(
                    f"Skipping vector index for {obj.id}: all embedding attempts returned zeros."
                )
                continue

            metadata: Dict[str, Any] = {"type": obj.type.value, "title": obj.title or obj.id}
            if hasattr(obj, "component_category") and obj.component_category:
                metadata["category"] = obj.component_category
            if hasattr(obj, "component_subcategory") and obj.component_subcategory:
                metadata["subcategory"] = obj.component_subcategory
            if hasattr(obj, "platform_id") and obj.platform_id:
                metadata["platform_id"] = obj.platform_id
            if hasattr(obj, "vendor") and obj.vendor:
                metadata["vendor"] = obj.vendor
            if hasattr(obj, "generation") and obj.generation:
                metadata["generation"] = obj.generation
            if hasattr(obj, "solution_domain") and obj.solution_domain:
                metadata["solution_domain"] = obj.solution_domain
            if hasattr(obj, "lifecycle_status") and obj.lifecycle_status:
                metadata["lifecycle_status"] = obj.lifecycle_status.value

            ids_batch.append(obj.id)
            docs_batch.append(text_repr)
            metas_batch.append(metadata)
            embs_batch.append(embedding)

            # Flush to ChromaDB in batches
            if len(ids_batch) >= batch_size:
                try:
                    self.collection.upsert(
                        ids=ids_batch,
                        embeddings=embs_batch,
                        documents=docs_batch,
                        metadatas=metas_batch,
                    )  # type: ignore
                    indexed_count += len(ids_batch)
                    logger.debug(f"Upserted batch of {len(ids_batch)} into ChromaDB.")
                    ids_batch, docs_batch, metas_batch, embs_batch = [], [], [], []
                except Exception as e:
                    logger.error(f"Failed to upsert batch to ChromaDB: {e}")
                    ids_batch, docs_batch, metas_batch, embs_batch = [], [], [], []

        # Flush remaining
        if ids_batch:
            try:
                self.collection.upsert(
                    ids=ids_batch,
                    embeddings=embs_batch,
                    documents=docs_batch,
                    metadatas=metas_batch,
                )  # type: ignore
                indexed_count += len(ids_batch)
                logger.debug(f"Upserted final batch of {len(ids_batch)} into ChromaDB.")
            except Exception as e:
                logger.error(f"Failed to upsert final batch to ChromaDB: {e}")

        logger.info(
            f"index_many: {len(indexable)} eligible, {indexed_count} successfully indexed."
        )
        return indexed_count

    @staticmethod
    def _text_repr(obj: BaseEngineeringObject) -> str:
        """Build a rich text representation for embedding. More context = better search quality."""
        parts = [f"Type: {obj.type.value}", f"Title: {obj.title or obj.id}"]

        if hasattr(obj, "description") and obj.description:
            parts.append(f"Description: {obj.description}")
        if hasattr(obj, "platform_id") and obj.platform_id:
            parts.append(f"Platform: {obj.platform_id}")
        if hasattr(obj, "component_category") and obj.component_category:
            parts.append(f"Category: {obj.component_category}")
        if hasattr(obj, "component_subcategory") and obj.component_subcategory:
            parts.append(f"Subcategory: {obj.component_subcategory}")
        if hasattr(obj, "vendor") and obj.vendor:
            parts.append(f"Vendor: {obj.vendor}")
        if hasattr(obj, "generation") and obj.generation:
            parts.append(f"Generation: {obj.generation}")
        if hasattr(obj, "part_number") and getattr(obj, "part_number", None):
            parts.append(f"Part Number: {obj.part_number}")
        if hasattr(obj, "attributes") and obj.attributes:
            attr_strings = [
                f"{attr.name}: {attr.value}{' ' + attr.unit if attr.unit else ''}"
                for attr in obj.attributes
            ]
            parts.append("Attributes:\n- " + "\n- ".join(attr_strings))
        if hasattr(obj, "capabilities") and obj.capabilities:
            parts.append("Capabilities:\n- " + "\n- ".join(obj.capabilities))
        if hasattr(obj, "tags") and obj.tags:
            parts.append(f"Tags: {', '.join(obj.tags)}")
        return "\n".join(parts)

    def semantic_search(
        self,
        query: str,
        n_results: int = 50,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[str, float]]:
        """Search the vector database and return a list of matching IDs with confidence scores."""
        embeddings = self.llm.generate_embeddings([query])
        embedding = embeddings[0]

        if all(v == 0.0 for v in embedding):
            logger.warning("Query embedding failed. Falling back to empty results.")
            return []

        try:
            # Clamp n_results to actual collection size to avoid ChromaDB error
            actual_count = self.collection.count()
            if actual_count == 0:
                return []
            n_results = min(n_results, actual_count)

            query_kwargs: Dict[str, Any] = {
                "query_embeddings": [embedding],
                "n_results": n_results,
            }
            # Only pass where clause when filter_metadata is non-empty
            if filter_metadata:
                query_kwargs["where"] = filter_metadata

            results = self.collection.query(**query_kwargs)  # type: ignore

            if results and "ids" in results and results["ids"]:
                ids = results["ids"][0]
                distances_raw = results.get("distances")
                distances = distances_raw[0] if distances_raw else [0.0] * len(ids)

                # Convert L2 distance to a 0.0 - 1.0 confidence score
                scores = [max(0.0, 1.0 - (d / 2.0)) for d in distances]
                return list(zip(ids, scores))
            return []
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []

    def reindex_all(self, objects: List[BaseEngineeringObject]) -> int:
        """
        Phase 2: Full rebuild of the ChromaDB collection from scratch.
        Drops existing data and re-indexes all provided objects.
        Returns the count of objects successfully indexed.
        """
        logger.info(f"[Phase 2] reindex_all() called with {len(objects)} objects — clearing collection first")
        try:
            # Drop and recreate to start fresh
            client = self.collection._client  # type: ignore[attr-defined]
            collection_name = self.collection.name
            client.delete_collection(collection_name)
            self.collection = client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "l2"},
            )
            logger.info(f"[Phase 2] Collection '{collection_name}' cleared. Re-indexing {len(objects)} objects.")
        except Exception as e:
            logger.warning(f"[Phase 2] Could not drop collection for full rebuild: {e}. Continuing with upsert.")

        indexed = self.index_many(objects)
        logger.info(f"[Phase 2] reindex_all() complete: {indexed}/{len(objects)} objects indexed")
        return indexed
