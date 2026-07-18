"""
API endpoint tests.

These use the `api_client` fixture (see conftest.py), which points the API
at a tmp_path-backed repository seeded with fixture data. This suite must
NEVER import `ikp_platform.api.app` directly and call it without that
fixture -- doing so runs RepoManager.bootstrap() against the real project's
`repository/` folder and overwrites the real STATE.md as a side effect.
"""


def test_query_endpoint(api_client):
    response = api_client.post(
        "/api/query",
        json={"query": "I need an AI server with a GPU and NVMe"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "candidates" in data
    assert isinstance(data["candidates"], list)
    assert len(data["candidates"]) > 0
    assert "solution_id" in data["candidates"][0]


def test_health_endpoint(api_client):
    response = api_client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["stats"]["total_nodes"] >= 2
    assert data["repository_seeded"] is True
