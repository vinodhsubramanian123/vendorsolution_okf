import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, List

from mcp.server import Server
import mcp.types as types
from mcp.server.stdio import stdio_server

from ikp_platform.core.repository.repo_manager import RepoManager
from ikp_platform.core.reasoning.intent_parser import IntentParser
from ikp_platform.core.reasoning.solution_generator import SolutionGenerator

# Setup basic logging to file since stdout is used by MCP
logging.basicConfig(
    filename="mcp_server.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("mcp_ikp")

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
REPOSITORY_PATH = PROJECT_ROOT / "repository"

app = Server("ikp-mcp-server")

_repo_instance = None

def get_repo() -> RepoManager:
    global _repo_instance
    if _repo_instance is None:
        logger.info("Initializing global RepoManager for MCP Server")
        _repo_instance = RepoManager(str(REPOSITORY_PATH), str(PROJECT_ROOT))
        _repo_instance.bootstrap()
    return _repo_instance

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="query_ikp_solution",
            description="Query the Infrastructure Knowledge Platform to generate an engineering bill of materials (BOM) based on a natural language request.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language request, e.g., 'I need an AI server with a GPU and NVMe storage'"
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="get_platform_status",
            description="Get the current statistics of the IKP knowledge graph (number of nodes, edges, and object types).",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls."""
    logger.info(f"Tool called: {name} with args {arguments}")
    
    try:
        if name == "query_ikp_solution":
            query = arguments.get("query")
            if not query:
                return [types.TextContent(type="text", text="Missing 'query' argument.")]
                
            # Initialize backend
            repo = get_repo()
            
            parser = IntentParser()
            request = parser.parse_request(query)
            
            generator = SolutionGenerator(repo.graph, repo.vector_store)
            candidates = generator.generate(request)
            
            if not candidates:
                return [types.TextContent(type="text", text="No valid solutions found.")]
                
            # Format output
            output = f"Generated {len(candidates)} solution candidates:\n\n"
            for i, cand in enumerate(candidates, 1):
                output += f"--- Candidate {i} ({cand.profile}) ---\n"
                output += f"Status: {cand.validation_status}\n"
                output += f"Confidence: {cand.confidence.value}\n"
                output += "Components:\n"
                for comp in cand.components:
                    output += f"  - {comp}\n"
                output += "\n"
                
            return [types.TextContent(type="text", text=output)]
            
        elif name == "get_platform_status":
            repo = get_repo()
            stats = repo.graph.get_stats()
            
            output = "IKP Platform Status:\n"
            output += f"- Total Objects: {stats['total_nodes']}\n"
            output += f"- Relationships: {stats['total_edges']}\n"
            if "type_counts" in stats:
                output += "- Object Types:\n"
                for obj_type, count in stats["type_counts"].items():
                    output += f"  - {obj_type}: {count}\n"
                    
            return [types.TextContent(type="text", text=output)]
            
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
            
    except Exception as e:
        logger.error(f"Error executing {name}: {str(e)}", exc_info=True)
        return [types.TextContent(type="text", text=f"Error executing {name}: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
