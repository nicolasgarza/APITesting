from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "postgresql+asyncpg://postgres:ally@localhost:1234/postgres"

engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
