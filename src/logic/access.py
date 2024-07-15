from aiogram.types import User as AIOgramUser
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from create_bot import bot
from database import engine
from database.models import User
from utils.exceptions import AlreadyRegistered
from database.dataclasses import User as UserDC


async def buy_access(user: AIOgramUser, months: int):
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})
        if u.whitelisted_till is not None:
            await u.add_time(months)
        else:
            await u.create_time(months)
        
        await s.commit()
