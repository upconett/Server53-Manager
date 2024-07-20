# Python модули
from aiogram.types import User as AIOgramUser
from sqlalchemy.ext.asyncio import AsyncSession


# Локальные модули
from database import engine
from database.models import User, Access


# Функции
async def buy_access(user: AIOgramUser, months: int):
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})

        if u.access is not None:
            await u.access.add_time(months)
        else:
            u.access = Access(months)

        await s.commit()
