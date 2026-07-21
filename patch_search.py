with open("ikp_platform/core/repository/repo_manager.py", "r") as f:
    content = f.read()

target = """    def search(self, query: str, limit: int = 10, filter_metadata: Optional[dict] = None) -> List[Dict]:
        \"\"\"Hybrid search combining Graph structure and Vector semantic similarity.\"\"\"
        from .graph_builder import GraphBuilder
        
        # 1. Start with semantic search
        semantic_results = self.vector_store.semantic_search(query, n_results=limit * 2, filter_metadata=filter_metadata)
        
        # 2. Extract specific metadata if searching within a platform
        platform_id = filter_metadata.get("platform_id") if filter_metadata else None
        target_category = filter_metadata.get("component_category") if filter_metadata else None
        
        hybrid_results = []
        builder = GraphBuilder(self.graph)"""

replacement = """    def search(self, query: str, limit: int = 10, filter_metadata: Optional[dict] = None) -> List[Dict]:
        \"\"\"Hybrid search combining Graph structure and Vector semantic similarity.\"\"\"
        import logging
        logger = logging.getLogger(__name__)
        
        # 1. Start with semantic search
        try:
            semantic_results = self.vector_store.semantic_search(query, n_results=limit * 2, filter_metadata=filter_metadata)
        except Exception as e:
            logger.warning(f"Vector search failed: {e}. Falling back to graph search.")
            semantic_results = []
            
        # Fallback to simple text matching on the graph if semantic search returned nothing (e.g., rate limit)
        if not semantic_results:
            for node, data in self.graph.graph.nodes(data=True):
                title = data.get("title", "")
                desc = data.get("description", "")
                if query.lower() in title.lower() or query.lower() in desc.lower():
                    semantic_results.append((node, 0.5)) # default fallback score
        
        # 2. Extract specific metadata if searching within a platform
        platform_id = filter_metadata.get("platform_id") if filter_metadata else None
        target_category = filter_metadata.get("component_category") if filter_metadata else None
        
        hybrid_results = []"""

if target in content:
    content = content.replace(target, replacement)
    with open("ikp_platform/core/repository/repo_manager.py", "w") as f:
        f.write(content)
    print("Patched repo_manager.py")
else:
    print("Target not found in repo_manager.py")
