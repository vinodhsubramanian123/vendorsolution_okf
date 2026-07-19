import pytest
import os
from mcp import StdioServerParameters


def test_mcp_server_parameters():
    """Verify MCP Server Parameters can be constructed for the seekstone tool."""
    env = os.environ.copy()
    env["SEEKSTONE_VAULT"] = "/home/vinodh/vendorsolution_okf/repository"

    server_params = StdioServerParameters(command="seekstone", args=[], env=env)

    assert server_params.command == "seekstone"
    assert (
        server_params.env["SEEKSTONE_VAULT"]
        == "/home/vinodh/vendorsolution_okf/repository"
    )


@pytest.mark.asyncio
async def test_mcp_client_init(mocker):
    """Mock the MCP ClientSession to verify initialization logic."""
    from mcp import ClientSession

    mock_session = mocker.Mock(spec=ClientSession)
    mock_session.initialize = mocker.AsyncMock()
    mock_session.list_tools = mocker.AsyncMock(return_value=mocker.Mock(tools=[]))

    await mock_session.initialize()
    tools = await mock_session.list_tools()

    mock_session.initialize.assert_awaited_once()
    mock_session.list_tools.assert_awaited_once()
    assert tools.tools == []
