# Python модули
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import logging


# Локальные модули
import config
from database.models import Base


# Переменные
engine = create_async_engine('sqlite+aiosqlite:///{0}'.format(config.DBFILE))


# Функции
async def check_tables():
    async with AsyncSession(engine) as s:
        async with s.bind.connect() as conn:
            tables = await conn.run_sync(s.bind.dialect.get_table_names)
            logging.info(f'Existing tables: {str(tables)}')
            if 'users' not in tables:
                logging.info('Creating users table...')
                await conn.run_sync(Base.metadata.create_all)
