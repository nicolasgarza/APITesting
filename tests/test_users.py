from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from main import app as fastapi_app
import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient
from app.routers.user_router import get_session as get_db

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_async_engine("postgresql+asyncpg://postgres:ally@localhost:1234/postgres"), class_=AsyncSession)

@pytest.fixture(scope="function")
async def override_get_db():
   async with SessionLocal() as db:
        db.begin_ntested()
        try:
           yield db
        finally:
           await db.rollback()

@pytest.fixture(scope="function")
def test_app(override_get_db):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    return fastapi_app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def async_client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test", headers={"Content-Type": "application/json"}) as ac:
        yield ac

pytestmark = pytest.mark.asyncio

async def test_read_user(async_client):
    response = await async_client.get("/users/7")
    assert response.status_code == 200
    assert response.json() == {
        "email": "7user@example.com",
        "username": "user3",
        "id": 7
    }

async def test_create_user(async_client):
    response = await async_client.post("/users", json={
        "email": "pytestuser2@example.com",
        "username": "test2usertest",
        "password": "testpasstest"
    })
    assert response.status_code == 200
    assert response.json() == {
        "email": "pytestuser2@example.com",
        "username": "test2usertest",
    }


async def test_get_user_not_found(async_client):
    response = await async_client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

async def test_create_user_duplicate_email(async_client):
    # Assuming a user with the email "existing@example.com" already exists
    response = await async_client.post("/users", json={
        "email": "existing@example.com",
        "username": "newuser",
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

async def test_update_user(async_client, test_user_token):
    # Assuming you have a fixture that creates a test user and returns its token
    response = await async_client.put(
        f"/users/{test_user_token.user_id}",
        json={"email": "updated@example.com"},
        headers={"Authorization": f"Bearer {test_user_token.access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "updated@example.com"

async def test_update_user_unauthorized(async_client, test_user_token):
    # Trying to update a different user's info
    response = await async_client.put(
        "/users/999",
        json={"email": "updated@example.com"},
        headers={"Authorization": f"Bearer {test_user_token.access_token}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized to update this user"}

async def test_delete_user(async_client, test_user_token):
    response = await async_client.delete(
        f"/users/{test_user_token.user_id}",
        headers={"Authorization": f"Bearer {test_user_token.access_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted successfully"}

async def test_delete_user_unauthorized(async_client, test_user_token):
    # Trying to delete a different user
    response = await async_client.delete(
        "/users/999",
        headers={"Authorization": f"Bearer {test_user_token.access_token}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized to delete this user"}