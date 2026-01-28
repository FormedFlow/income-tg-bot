from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.models.base import Base
from core.config import base_settings
import asyncio


engine = create_async_engine(base_settings.db_url_base_async,
                             echo=True)
async_seshmaker = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_tables())
