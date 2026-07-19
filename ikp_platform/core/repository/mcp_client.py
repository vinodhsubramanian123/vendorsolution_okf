import asyncio
import logging
import os
import shutil
from typing import List
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger("ikp.repository.mcp")


class ObsidianMCPClient:
    """
    Client for interacting with the Obsidian MCP server (seekstone).
    Provides parallel/fallback search capabilities over the markdown vault.

    Requires the `seekstone` binary on PATH -- genuinely optional, most
    environments won't have it. `is_available()` lets callers (and
    search() itself) skip the subprocess-spawn/thread overhead entirely
    in the common case where it isn't installed, rather than paying that
    cost on every call just to fail closed.
    """

    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        # Inherit PATH from parent environment instead of hardcoding
        env = dict(os.environ)
        env["SEEKSTONE_VAULT"] = self.vault_path
        self.server_params = StdioServerParameters(
            command="seekstone",
            args=[],
            env=env,
        )

    def is_available(self) -> bool:
        """Whether the seekstone binary can actually be found on PATH."""
        return shutil.which("seekstone") is not None

    async def _search_async(self, query: str) -> List[str]:
        results = []
        try:
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    response = await session.call_tool(
                        "search", arguments={"query": query}
                    )

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
                                                file_path = (
                                                    self.vault_path + "/" + item["path"]
                                                )
                                                # Read frontmatter to get ID
                                                try:
                                                    with open(
                                                        file_path, "r", encoding="utf-8"
                                                    ) as f:
                                                        content = f.read()
                                                    if content.startswith("---"):
                                                        fm_text = content.split(
                                                            "---", 2
                                                        )[1]
                                                        import yaml

                                                        fm = yaml.safe_load(fm_text)
                                                        if fm and "id" in fm:
                                                            results.append(fm["id"])
                                                            continue
                                                except Exception:
                                                    logger.debug(
                                                        f"Failed to parse frontmatter for {file_path}"
                                                    )
                                                # Fallback to filename
                                                results.append(
                                                    item["path"]
                                                    .split("/")[-1]
                                                    .replace(".md", "")
                                                )
                                except json.JSONDecodeError:
                                    logger.debug(
                                        "Failed to decode JSON from MCP response"
                                    )
        except Exception as e:
            logger.error(f"MCP Search failed: {e}")

        return list(set(results))

    def search(self, query: str) -> List[str]:
        """
        Synchronous wrapper to execute a search against the vault.
        Returns a list of relative paths matching the search.
        """
        if not self.is_available():
            logger.debug("seekstone binary not found on PATH; skipping MCP search.")
            return []

        logger.info(f"Executing Obsidian MCP search for: {query}")
        try:
            _ = asyncio.get_running_loop()
            is_running = True
        except RuntimeError:
            is_running = False

        if is_running:
            import threading

            result = []

            def _run():
                result.append(asyncio.run(self._search_async(query)))

            t = threading.Thread(target=_run)
            t.start()
            t.join()
            return result[0]
        else:
            return asyncio.run(self._search_async(query))
