from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from configs.common_config import settings
from core.constants import DB_NAMING_CONVENTION
from core.utils.common_utils import get_async_db_uri

# Convert the database URI to async format
# Replace 'postgresql://' with 'postgresql+asyncpg://'
# Replace 'mysql://' with 'mysql+asyncmy://'
DATABASE_URI = str(settings.DATABASE_URI)
DATABASE_URI = get_async_db_uri(DATABASE_URI)

# Create async engine
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)
engine = create_async_engine(
    DATABASE_URI,
    echo=False,  # Set to True for debugging SQL queries
    future=True,
)

# Create base class for declarative models
Base = declarative_base(metadata=metadata)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Dependency for FastAPI
async def async_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
