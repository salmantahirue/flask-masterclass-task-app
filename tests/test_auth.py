"""
Simple tests for auth API: register and login.
Run: pytest tests/ -v
"""
import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as c:
        with app.app_context():
            db.create_all()
            yield c


def test_register(client):
    """Register returns 201 and includes user and token."""
    r = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "password123", "username": "Test"},
        content_type="application/json",
    )
    assert r.status_code == 201
    data = r.get_json()
    assert "user" in data
    assert "token" in data
    assert data["user"]["email"] == "test@example.com"


def test_register_duplicate_email(client):
    """Register with same email returns 400."""
    client.post(
        "/api/auth/register",
        json={"email": "same@example.com", "password": "password123"},
        content_type="application/json",
    )
    r = client.post(
        "/api/auth/register",
        json={"email": "same@example.com", "password": "other123"},
        content_type="application/json",
    )
    assert r.status_code == 400
    assert "error" in r.get_json()


def test_login(client):
    """Login after register returns 200 and token."""
    client.post(
        "/api/auth/register",
        json={"email": "login@example.com", "password": "secret123"},
        content_type="application/json",
    )
    r = client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "secret123"},
        content_type="application/json",
    )
    assert r.status_code == 200
    data = r.get_json()
    assert "token" in data
    assert data["user"]["email"] == "login@example.com"


def test_login_wrong_password(client):
    """Login with wrong password returns 401."""
    client.post(
        "/api/auth/register",
        json={"email": "wrong@example.com", "password": "correct123"},
        content_type="application/json",
    )
    r = client.post(
        "/api/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpass"},
        content_type="application/json",
    )
    assert r.status_code == 401
    assert "error" in r.get_json()


def test_protected_without_token(client):
    """GET /api/auth/profile without token returns 401."""
    r = client.get("/api/auth/profile")
    assert r.status_code == 401
