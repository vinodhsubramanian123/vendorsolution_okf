import pytest
from fastapi.testclient import TestClient
from ikp_platform.api import app

client = TestClient(app)

def test_query_endpoint():
    response = client.post(
        "/api/query",
        json={"query": "I need an AI server with a GPU and NVMe"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "candidates" in data
    assert isinstance(data["candidates"], list)
    assert len(data["candidates"]) > 0
    assert "solution_id" in data["candidates"][0]

def test_health_endpoint():
    response = client.get("/api/status")
    assert response.status_code == 200
