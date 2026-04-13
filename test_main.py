import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database import Base, get_db
from main import app
import services
from unittest.mock import AsyncMock

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

# Mock the external API service
@pytest.fixture(autouse=True)
def mock_validator(monkeypatch):
    mock = AsyncMock(return_value={"id": 123, "title": "Mock Artwork"})
    monkeypatch.setattr(services, "validate_artwork_id", mock)
    return mock

def test_create_project_with_places():
    response = client.post(
        "/projects/",
        json={
            "name": "Test Project",
            "description": "Test Desc",
            "places": [{"external_id": 123, "notes": "Some note"}]
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project"
    assert len(data["places"]) == 1
    assert data["places"][0]["external_id"] == 123

def test_create_project_duplicate_places_fails():
    response = client.post(
        "/projects/",
        json={
            "name": "Duplicate Test",
            "places": [
                {"external_id": 123},
                {"external_id": 123}
            ]
        }
    )
    assert response.status_code == 400
    assert "Duplicate external IDs" in response.json()["detail"]

def test_delete_project_visited_fails():
    client.post("/projects/", json={"name": "Delete Test", "places": [{"external_id": 123}]})

    client.patch("/projects/1/places/1", params={"visited": True})

    response = client.delete("/projects/1")
    assert response.status_code == 400
    assert "Cannot delete project" in response.json()["detail"]

def test_project_auto_completion():
    client.post(
        "/projects/",
        json={
            "name": "Completion Test",
            "places": [{"external_id": 1}, {"external_id": 2}]
        }
    )

    proj = client.get("/projects/1").json()
    assert proj["is_completed"] is False

    client.patch("/projects/1/places/1", params={"visited": True})
    assert client.get("/projects/1").json()["is_completed"] is False

    client.patch("/projects/1/places/2", params={"visited": True})
    assert client.get("/projects/1").json()["is_completed"] is True

    client.patch("/projects/1/places/1", params={"visited": False})
    assert client.get("/projects/1").json()["is_completed"] is False

def test_max_places_limit():
    places = [{"external_id": i} for i in range(11)]
    response = client.post("/projects/", json={"name": "Over Limit", "places": places})
    assert response.status_code == 400
    assert "maximum of 10 places" in response.json()["detail"]

def test_add_place_to_existing_project():
    client.post("/projects/", json={"name": "Existing Proj"})
    response = client.post("/projects/1/places/", json={"external_id": 456, "notes": "Added later"})
    assert response.status_code == 201
    assert response.json()["external_id"] == 456

    proj = client.get("/projects/1").json()
    assert len(proj["places"]) == 1
