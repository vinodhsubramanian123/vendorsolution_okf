import chromadb
from chromadb.config import Settings
from pathlib import Path
import logging
from typing import List, Dict, Any, Optional
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
        
    def index_object(self, obj: BaseEngineeringObject):
        """Vectorize and index a single object."""
        # We only index Platforms and Components for semantic search
        if obj.type.value not in ["Platform", "Component"]:
            return
            
        # Create a rich text representation for embedding
        text_repr = f"Type: {obj.type.value}\nTitle: {obj.title or obj.id}\n"
        if hasattr(obj, "component_category") and obj.component_category:
            text_repr += f"Category: {obj.component_category}\n"
        if hasattr(obj, "attributes") and obj.attributes:
            text_repr += f"Attributes: {', '.join(f'{attr.name}={attr.value}' for attr in obj.attributes)}\n"
            
        # Generate embedding
        embeddings = self.llm.generate_embeddings([text_repr])
        embedding = embeddings[0]
        
        # Don't index if embedding failed (all zeros)
        if all(v == 0.0 for v in embedding):
            logger.warning(f"Skipping vector index for {obj.id} due to embedding failure.")
            return
            
        # Store in ChromaDB
        metadata = {
            "type": obj.type.value,
            "title": obj.title or obj.id
        }
        if hasattr(obj, "component_category") and obj.component_category:
            metadata["category"] = obj.component_category
            
        try:
            self.collection.upsert(
                ids=[obj.id],
                embeddings=[embedding],
                documents=[text_repr],
                metadatas=[metadata]
            )
            logger.debug(f"Vectorized and indexed: {obj.id}")
        except Exception as e:
            logger.error(f"Failed to index {obj.id} in ChromaDB: {e}")
            
    def semantic_search(self, query: str, n_results: int = 50, filter_metadata: Optional[Dict[str, Any]] = None) -> List[str]:
        """Search the vector database and return a list of matching IDs."""
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
                return results["ids"][0]
            return []
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []
