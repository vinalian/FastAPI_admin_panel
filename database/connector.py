from os import environ
from dotenv import load_dotenv
from database.models import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

import asyncio

load_dotenv()

host = environ.get('DB_HOST')
port = environ.get('DB_PORT')
user = environ.get('DB_USER')
password = environ.get('DB_PASSWORD')
db_name = environ.get('DB_NAME')


DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_models():
    """
    Create tables.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """
    Function create and return Sqlalchemy session.
    :return: Sqlalchemy async session.
    """
    async with async_session() as session:
        return session


if __name__ == '__main__':
    asyncio.run(init_models())
