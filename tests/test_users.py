from fastapi.testclient import TestClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from main import app as fastapi_app
from typing import AsyncGenerator
import pytest
from httpx import AsyncClient

# Assuming environment variable or separate config for test database URI
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:ally@localhost:1234/test_db"

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=create_async_engine(TEST_DATABASE_URL, echo=True),
    class_=AsyncSession
)

# Dependency to get the database session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@pytest.fixture(scope="function")
async def override_get_db():
    async with SessionLocal() as db:
        # Use a savepoint for test isolation
        sp = await db.begin_nested()
        await db.begin()  # This starts the transaction for the test
        try:
            yield db
        finally:
            await db.rollback()  # This rolls back any changes after the yield
            await sp.rollback()  # This rolls back the savepoint if needed

@pytest.fixture(scope="function")
def test_app(override_get_db):
    fastapi_app.dependency_overrides[get_session] = override_get_db
    return fastapi_app

# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()

@pytest_asyncio.fixture(scope="function")
async def async_client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test", headers={"Content-Type": "application/json"}) as ac:
        yield ac

# Tests remain the same

pytestmark = pytest.mark.asyncio

@pytest.fixture(scope="function")
async def test_user(override_get_db):
    async for db in override_get_db:
        from app.models import User
        user = User(email="test@test.com", username="testuser", hashed_password="testpass")
        db.add(user)
        await db.commit()  # Explicitly commit to ensure visibility
        try:
            yield user
        finally:
            await db.delete(user)
            await db.commit()  # Clean up after the test


@pytest.mark.asyncio
async def test_read_user(async_client, test_user):
    print("-----------------")
    print(test_user.id)
    print("-----------------")
    response = await async_client.get(f"/users/{test_user.id}")
    assert response.json() == {
        "email": test_user.email,
        "username": test_user.username,
        "id": test_user.id
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