"""
Integration tests for the Habit Tracker API.

Run with:
    pip install pytest httpx
    pytest tests/ -v
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db
from app.main import app
from app.models import Base

# ─── Test DB setup ────────────────────────────────────────────────────────────

TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
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


# ─── Helpers ──────────────────────────────────────────────────────────────────

def register_and_login(email="test@example.com", password="password123"):
    client.post("/auth/register", json={
        "email": email, "username": "testuser", "password": password
    })
    resp = client.post("/auth/login", data={"username": email, "password": password})
    return resp.json()["access_token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ─── Auth tests ───────────────────────────────────────────────────────────────

def test_register():
    r = client.post("/auth/register", json={
        "email": "user@example.com",
        "username": "newuser",
        "password": "password123",
    })
    assert r.status_code == 201
    assert r.json()["email"] == "user@example.com"


def test_register_duplicate_email():
    payload = {"email": "dup@example.com", "username": "u1", "password": "password123"}
    client.post("/auth/register", json=payload)
    payload["username"] = "u2"
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 400


def test_login_success():
    token = register_and_login()
    assert token is not None


def test_login_wrong_password():
    register_and_login()
    r = client.post("/auth/login", data={
        "username": "test@example.com", "password": "wrongpassword"
    })
    assert r.status_code == 401


# ─── Habit tests ──────────────────────────────────────────────────────────────

def test_create_habit():
    token = register_and_login()
    r = client.post("/habits/", json={"title": "Read books"}, headers=auth_headers(token))
    assert r.status_code == 201
    assert r.json()["title"] == "Read books"


def test_list_habits():
    token = register_and_login()
    h = auth_headers(token)
    client.post("/habits/", json={"title": "H1"}, headers=h)
    client.post("/habits/", json={"title": "H2"}, headers=h)
    r = client.get("/habits/", headers=h)
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_update_habit():
    token = register_and_login()
    h = auth_headers(token)
    habit_id = client.post("/habits/", json={"title": "Old"}, headers=h).json()["id"]
    r = client.patch(f"/habits/{habit_id}", json={"title": "New"}, headers=h)
    assert r.status_code == 200
    assert r.json()["title"] == "New"


def test_delete_habit():
    token = register_and_login()
    h = auth_headers(token)
    habit_id = client.post("/habits/", json={"title": "Delete me"}, headers=h).json()["id"]
    r = client.delete(f"/habits/{habit_id}", headers=h)
    assert r.status_code == 204
    assert client.get(f"/habits/{habit_id}", headers=h).status_code == 404


# ─── Log tests ────────────────────────────────────────────────────────────────

def test_check_in():
    token = register_and_login()
    h = auth_headers(token)
    habit_id = client.post("/habits/", json={"title": "Exercise"}, headers=h).json()["id"]
    r = client.post(f"/habits/{habit_id}/logs/", json={"logged_date": "2024-01-15"}, headers=h)
    assert r.status_code == 201
    assert r.json()["logged_date"] == "2024-01-15"


def test_duplicate_check_in():
    token = register_and_login()
    h = auth_headers(token)
    habit_id = client.post("/habits/", json={"title": "Exercise"}, headers=h).json()["id"]
    payload = {"logged_date": "2024-01-15"}
    client.post(f"/habits/{habit_id}/logs/", json=payload, headers=h)
    r = client.post(f"/habits/{habit_id}/logs/", json=payload, headers=h)
    assert r.status_code == 409


# ─── Stats tests ──────────────────────────────────────────────────────────────

def test_stats_empty():
    token = register_and_login()
    h = auth_headers(token)
    habit_id = client.post("/habits/", json={"title": "Meditate"}, headers=h).json()["id"]
    r = client.get(f"/stats/{habit_id}", headers=h)
    assert r.status_code == 200
    data = r.json()
    assert data["current_streak"] == 0
    assert data["total_completions"] == 0
