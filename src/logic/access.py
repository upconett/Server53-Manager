# Python модули
from aiogram.types import User as AIOgramUser
from sqlalchemy.ext.asyncio import AsyncSession


# Локальные модули
from database import engine
from database.models import User, Access


# Функции
async def buy_access(user: AIOgramUser, days: int = 31):
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})

        if u.access is not None:
            await u.access.add_time(days)
        else:
            u.access = Access(days)

        await s.commit()
