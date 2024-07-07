from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import inspect
import asyncio

import config
from database.models import Base

engine = create_async_engine('sqlite+aiosqlite:///{0}'.format(config.DBFILE))


async def check_tables():
    async with AsyncSession(engine) as s:
        async with s.bind.connect() as conn:
            tables = await conn.run_sync(s.bind.dialect.get_table_names)
            print('Existing tables:', tables)
            if 'users' not in tables:
                print('Creating users table...')
                await conn.run_sync(Base.metadata.create_all)
