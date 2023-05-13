import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

name = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
port = os.getenv('DB_PORT')
host = os.getenv('DB_HOST')


async def create_sessionmaker():
    '''return async_session object'''
    engine = create_async_engine(f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}",
                                 echo=False
                                 )
    
    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession, future=True
    )
    return async_sessionmaker

