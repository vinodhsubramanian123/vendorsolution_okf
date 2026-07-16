import asyncio
import logging
from typing import List, Dict, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger("ikp.repository.mcp")

class ObsidianMCPClient:
    """
    Client for interacting with the Obsidian MCP server (seekstone).
    Provides parallel/fallback search capabilities over the markdown vault.
    """
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.server_params = StdioServerParameters(
            command="seekstone",
            args=[],
            env={
                "SEEKSTONE_VAULT": self.vault_path,
                # Ensure node/npm are in path
                "PATH": "/home/vinodh/.nvm/versions/node/v22.22.3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            }
        )

    async def _search_async(self, query: str) -> List[str]:
        results = []
        try:
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    response = await session.call_tool("search", arguments={"query": query})
                    
                    if response and response.content:
                        for content_block in response.content:
                            if hasattr(content_block, "text"):
                                import json
                                try:
                                    # Seekstone 'search' tool usually returns a JSON string in the text field
                                    data = json.loads(content_block.text)
                                    if isinstance(data, list):
                                        for item in data:
                                            if "path" in item:
                                                file_path = self.vault_path + "/" + item["path"]
                                                # Read frontmatter to get ID
                                                try:
                                                    with open(file_path, "r", encoding="utf-8") as f:
                                                        content = f.read()
                                                    if content.startswith("---"):
                                                        fm_text = content.split("---", 2)[1]
                                                        import yaml
                                                        fm = yaml.safe_load(fm_text)
                                                        if fm and "id" in fm:
                                                            results.append(fm["id"])
                                                            continue
                                                except Exception:
                                                    logger.debug(f"Failed to parse frontmatter for {file_path}")
                                                # Fallback to filename
                                                results.append(item["path"].split("/")[-1].replace(".md", ""))
                                except json.JSONDecodeError:
                                    logger.debug("Failed to decode JSON from MCP response")
        except Exception as e:
            logger.error(f"MCP Search failed: {e}")
            
        return list(set(results))

    def search(self, query: str) -> List[str]:
        """
        Synchronous wrapper to execute a search against the vault.
        Returns a list of relative paths matching the search.
        """
        logger.info(f"Executing Obsidian MCP search for: {query}")
        return asyncio.run(self._search_async(query))

