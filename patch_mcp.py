with open("ikp_platform/core/repository/mcp_client.py", "r") as f:
    content = f.read()

target = """    def search(self, query: str) -> List[str]:
        \"\"\"
        Synchronous wrapper to execute a search against the vault.
        Returns a list of relative paths matching the search.
        \"\"\""""

replacement = """    def search(self, query: str) -> List[str]:
        \"\"\"
        Synchronous wrapper to execute a search against the vault.
        Returns a list of relative paths matching the search.
        \"\"\"
        # Phase 6: Local cache layer with TTL
        if not hasattr(self, '_cache'):
            self._cache = {}
            self._cache_ttl = 300 # 5 minutes TTL
            
        import time
        now = time.time()
        
        # Phase 6: Fallback logic - Use cached results if portal is down or skip network
        if query in self._cache:
            cache_time, cached_result = self._cache[query]
            if now - cache_time < self._cache_ttl:
                logger.debug(f"Returning cached MCP result for: {query}")
                return cached_result
        
        if not self.check_health():
            logger.warning(f"Vendor portal down. Using stale cache or static rules for: {query}")
            if query in self._cache:
                return self._cache[query][1]
            return []
            
"""

if target in content:
    content = content.replace(target, replacement)
    
    # Need to update the end of search method to cache the results
    target2 = """            return result[0]
        else:
            return asyncio.run(self._search_async(query))"""
            
    replacement2 = """            final_result = result[0]
        else:
            final_result = asyncio.run(self._search_async(query))
            
        if hasattr(self, '_cache'):
            self._cache[query] = (time.time(), final_result)
        return final_result"""
        
    content = content.replace(target2, replacement2)

    with open("ikp_platform/core/repository/mcp_client.py", "w") as f:
        f.write(content)
    print("Patched mcp_client.py")
else:
    print("Target not found in mcp_client.py")
