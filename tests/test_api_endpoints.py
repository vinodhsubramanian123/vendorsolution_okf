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


def test_review_queue_approve(api_client):
    # First, get the review queue
    response = api_client.get("/api/review-queue")
    assert response.status_code == 200
    queue = response.json().get("queue", [])
    
    if queue:
        # If there are items, try to approve the first one
        obj_id = queue[0]["id"]
        approve_response = api_client.post(
            "/api/review-queue/approve",
            json={"object_id": obj_id}
        )
        assert approve_response.status_code == 200
        assert approve_response.json()["status"] == "success"
    else:
        # If the queue is empty, the endpoint should return 404 for a fake object
        approve_response = api_client.post(
            "/api/review-queue/approve",
            json={"object_id": "nonexistent-object"}
        )
        assert approve_response.status_code == 404
