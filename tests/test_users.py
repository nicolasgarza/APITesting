import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from fastapi import FastAPI, status
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from main import app as fastapi_app  # Ensure this imports correctly

# Assuming environment variable or separate config for test database URI
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:ally@localhost:1234/test_db"

# Setup the session maker
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

# Fixture for overriding the dependency with a session
@pytest.fixture(scope="function")
async def override_get_session():
    fastapi_app.dependency_overrides[get_session] = get_session
    yield
    fastapi_app.dependency_overrides.clear()

# Fixture to get the test app
@pytest.fixture(scope="function")
def test_app(override_get_session):
    return fastapi_app

# Fixture for async client
@pytest.fixture(scope="function")
async def async_client(test_app):
    async with AsyncClient(app=test_app, base_url="http://testserver", headers={"Content-Type": "application/json"}) as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_user(test_app: FastAPI, override_get_session):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        response = await ac.post("/users", json=user_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == "testuser"
        assert response.json()["email"] == "testuser@example.com"
