from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from aiogram.types import User as AIOgramUser
import os

import config
from create_bot import bot
from database import engine
from database.models import User, ImageMap


def extract_name(callback_data: str) -> str: 
    callback_data = callback_data.split('_')
    name = '_'.join(callback_data[1:])
    return name


async def unique_name(name: str) -> bool:
    async with AsyncSession(engine) as s:
        names = (await s.execute(select(ImageMap).where(ImageMap.name==name))).all()
        return len(names) == 0


async def download_image(name: str, file_id: str) -> None:
    name = name + '.png'
    path = os.path.join(config.IMAGES_PATH, name)
    await bot.download(file_id, path)


async def save_image(user: AIOgramUser, name: str, file_id: str) -> None:
    await download_image(name, file_id)
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})
        s.add(ImageMap(name=name, creator=u))
        await s.commit()
