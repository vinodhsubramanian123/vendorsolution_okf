import chromadb
from chromadb.config import Settings
from pathlib import Path
import logging
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
        """Vectorize and index a single object. Prefer index_many() for
        bulk ingestion -- this makes one embedding API call per call,
        which is what made ingesting the whole catalog require 100+
        blocking network round-trips."""
        return self.index_many([obj], batch_size=1)

    def index_many(self, objects: List[BaseEngineeringObject], batch_size: int = 20) -> int:
        """Vectorize and index a list of objects, batching embedding API
        calls in groups of `batch_size` instead of one call per object.
        Returns the number of objects successfully indexed."""
        indexable = [
            o for o in objects
            if o is not None and o.type.value in ["Platform", "Component", "SKU", "Rule", "SolutionCategory"]
        ]
        if not indexable:
            return 0

        indexed_count = 0
        for start in range(0, len(indexable), batch_size):
            batch = indexable[start:start + batch_size]
            text_reprs = [self._text_repr(o) for o in batch]

            embeddings = self.llm.generate_embeddings(text_reprs)

            ids, docs, metas, embs = [], [], [], []
            for obj, text_repr, embedding in zip(batch, text_reprs, embeddings):
                if all(v == 0.0 for v in embedding):
                    logger.warning(f"Skipping vector index for {obj.id} due to embedding failure.")
                    continue
                metadata = {"type": obj.type.value, "title": obj.title or obj.id}
                if hasattr(obj, "component_category") and obj.component_category:
                    metadata["category"] = obj.component_category
                ids.append(obj.id)
                docs.append(text_repr)
                metas.append(metadata)
                embs.append(embedding)

            if not ids:
                continue
            try:
                self.collection.upsert(ids=ids, embeddings=embs, documents=docs, metadatas=metas)
                indexed_count += len(ids)
                logger.debug(f"Vectorized and indexed batch of {len(ids)} objects.")
            except Exception as e:
                logger.error(f"Failed to index batch in ChromaDB: {e}")

        return indexed_count

    @staticmethod
    def _text_repr(obj: BaseEngineeringObject) -> str:
        text_repr = f"Type: {obj.type.value}\nTitle: {obj.title or obj.id}\n"
        if hasattr(obj, "component_category") and obj.component_category:
            text_repr += f"Category: {obj.component_category}\n"
        if hasattr(obj, "attributes") and obj.attributes:
            attr_strings = [f"{attr.name}: {attr.value}{' ' + attr.unit if attr.unit else ''}" for attr in obj.attributes]
            text_repr += "Attributes:\n- " + "\n- ".join(attr_strings) + "\n"
        if hasattr(obj, "capabilities") and obj.capabilities:
            text_repr += "Capabilities:\n- " + "\n- ".join(obj.capabilities) + "\n"
        if hasattr(obj, "tags") and obj.tags:
            text_repr += f"Tags: {', '.join(obj.tags)}\n"
        return text_repr

    def semantic_search(self, query: str, n_results: int = 50, filter_metadata: Optional[Dict[str, Any]] = None) -> List[Tuple[str, float]]:
        """Search the vector database and return a list of matching IDs with confidence scores."""
        embeddings = self.llm.generate_embeddings([query])
        embedding = embeddings[0]
        
        if all(v == 0.0 for v in embedding):
            logger.warning("Query embedding failed. Falling back to empty results.")
            return []
            
        try:
            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=n_results,
                where=filter_metadata
            )
            
            if results and "ids" in results and results["ids"]:
                ids = results["ids"][0]
                distances = results.get("distances", [[0.0] * len(ids)])[0]
                
                # Convert L2 distance to a 0.0 - 1.0 confidence score
                scores = [1.0 / (1.0 + d) for d in distances]
                return list(zip(ids, scores))
            return []
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []
