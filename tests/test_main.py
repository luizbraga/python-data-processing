"""Tests for FastAPI main application."""

from fastapi.testclient import TestClient


def test_read_root(client: TestClient) -> None:
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Python Data Processing API"}


def test_health_check(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_item(client: TestClient) -> None:
    """Test creating an item."""
    response = client.post(
        "/items", json={"name": "Test Item", "description": "A test item"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "A test item"
    assert "id" in data


def test_get_items(client: TestClient) -> None:
    """Test getting all items."""
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
