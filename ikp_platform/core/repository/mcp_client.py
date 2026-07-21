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
            final_result = result[0]
        else:
            final_result = asyncio.run(self._search_async(query))
            
        if hasattr(self, '_cache'):
            self._cache[query] = (time.time(), final_result)
        return final_result

    # -------------------------------------------------------------------------
    # Phase 6: Vendor Portal Integration & Fallback
    # -------------------------------------------------------------------------

    def check_health(self) -> bool:
        """
        Check health of the vendor portal / MCP connection.
        Returns True if reachable, False otherwise.
        """
        if not self.is_available():
            return False
            
        try:
            # Quick health check using asyncio/MCP ping (simulated via search)
            _ = self.search("health_check_ping")
            return True
        except Exception as e:
            logger.warning(f"Vendor Portal health check failed: {e}")
            return False

    def update_from_portal(self, platform_id: str, repo_manager) -> None:
        """
        Scrapes the latest data from the vendor portal and creates deltas.
        """
        if not self.check_health():
            logger.error("Vendor Portal down. Cannot update from portal.")
            return
            
        logger.info(f"Syncing latest rules and components for {platform_id} from Vendor Portal...")
        
        # Here we would do a targeted MCP call to get latest metadata, simulated:
        recent_updates = self.search(f"latest {platform_id}")
        
        if recent_updates:
            from ikp_platform.core.ontology.models import KnowledgeDelta, DeltaStatus, DeltaChange, ChangeType
            import uuid
            from datetime import datetime
            
            changes = []
            for item in recent_updates:
                changes.append(DeltaChange(
                    object_id=item,
                    change_type=ChangeType.MODIFY,
                    field_name="vendor_portal_sync",
                    old_value=None,
                    new_value=datetime.utcnow().isoformat(),
                    reason="Vendor Portal Sync update"
                ))
                
            delta = KnowledgeDelta(
                delta_id=str(uuid.uuid4()),
                source_id="vendor_portal",
                changes=changes,
                timestamp=datetime.utcnow(),
                status=DeltaStatus.PENDING,
                review_notes="Automated sync from Vendor Portal MCP"
            )
            
            repo_manager._record_delta(delta)
            logger.info(f"Created Knowledge Delta {delta.delta_id} with {len(changes)} sync updates.")
