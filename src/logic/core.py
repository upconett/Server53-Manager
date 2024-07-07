from aiogram.types import User as AIOgramUser
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine
from database.models import User


async def update_user(user: AIOgramUser) -> None:
    async with AsyncSession(engine) as s:
        db_user = await s.get(User, {'id': user.id})
        
        if db_user is None: s.add(User(user))
        else: await db_user.update(user)

        await s.commit()


async def get_nick(user: AIOgramUser) -> str | None:
    async with AsyncSession(engine) as s:
        db_user = await s.get(User, {'id': user.id})

        if db_user and db_user.nick:
            return db_user.nick
        return None
