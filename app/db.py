from collections.abc import AsyncGenerator
from datetime import datetime
import uuid
from sqlalchemy import Column,String,Text,DateTime,ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL="sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"
    # SQLite doesn't support the PostgreSQL UUID column type. Use a 36-char string UUID instead.
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

engine=create_async_engine(DATABASE_URL)
async_session_maker=async_sessionmaker(engine,expire_on_commit=False)

async def create_db_and_table():
    async with engine.begin() as conn:
        # use the metadata from our Base subclass so SQLAlchemy knows about our models
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session()->AsyncGenerator[AsyncSession,None]:
    async with async_session_maker() as session:
        yield session
 