import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from database.models import Base, Data1, Data2, Data3
from api.main import app

async def create_test_session():
    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db" 
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, class_=AsyncSession, autoflush=False, bind=engine)
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        query = text('SELECT COUNT(*) FROM data_1')
        count = await session.execute(query)
        count = count.scalar()

        if count == 0:
            data1 = Data1(name="Test data 1")
            session.add(data1)

            data2 = Data2(name="Test data 2")
            session.add(data2)

            data3 = Data3(name="Test data 3")
            session.add(data3)
            await session.commit()
            
    return TestingSessionLocal

@pytest.fixture
async def test_app():
    """Create and return a FastAPI application instance."""
    app.state.sessionmaker = await create_test_session()
    yield AsyncClient(app=app, base_url="http://test")



