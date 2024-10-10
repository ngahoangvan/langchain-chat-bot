from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from configs.common_config import settings
from core.constants import DB_NAMING_CONVENTION

DATABASE_URI = str(settings.DATABASE_URI)

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)
engine = create_engine(DATABASE_URI)
Base = declarative_base(metadata=metadata)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
