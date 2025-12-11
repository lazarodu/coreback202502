import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.infra.database import get_db
from core.infra.orm.base import Base
from core.main import app

# Use in-memory SQLite for tests with StaticPool to share connection
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    # Drop tables (cleanup)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # Use ASGITransport for direct app testing without running a server
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def token(client):
    # Register a user to get a token
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "Password123!",
    }
    await client.post("/api/users", json=user_data)

    # Login
    response = await client.post(
        "/api/token",
        data={"username": user_data["email"], "password": user_data["password"]},
    )
    return response.json()["access_token"]


@pytest_asyncio.fixture(scope="function")
async def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}
