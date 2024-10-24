import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app, get_db
import os

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"

engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture
async def test_db():
    # Create the test database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    # Clean up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def override_get_db(test_db):
    async def _override_get_db():
        try:
            yield test_db
        finally:
            await test_db.close()
    
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_item(override_get_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/items/", json={
            "name": "test_item",
            "description": "test description",
            "price": 10.5
        })
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test_item"
    assert data["price"] == 10.5

@pytest.mark.asyncio
async def test_read_item(override_get_db):
    # First create an item
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/items/", json={
            "name": "test_item",
            "description": "test description",
            "price": 10.5
        })
        
        response = await ac.get("/items/test_item")
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test_item"
    assert data["price"] == 10.5