from fastapi.testclient import TestClient
from main import app as fastapi_app
import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient

# client = TestClient(app)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def test_app():
    return fastapi_app

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
