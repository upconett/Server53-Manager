from aiogram.types import User as AIOgramUser
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from create_bot import bot
from database import engine
from database.models import User
from utils.exceptions import AlreadyRegistered
from database.dataclasses import User as UserDC


async def update_user(user: AIOgramUser) -> None:
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})

        if u is None: s.add(User(user))
        else: await u.update(user)

        await s.commit()


async def delete_extra(user: AIOgramUser, state_data: dict) -> None:
    """Удаляет все лишние сообщения"""
    for key in state_data:
        if 'id' in key:
            try:
                if isinstance(state_data[key], List):
                    await bot.delete_messages(
                        chat_id=user.id,
                        message_ids=state_data[key]
                    )
                else:
                    await bot.delete_message(
                        chat_id=user.id,
                        message_id=state_data[key]
                    )
            except:
                pass


async def get_user_data(user: AIOgramUser) -> UserDC:
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})
        if not u: return None
        return UserDC(u)


def extract_uuid_nick(message_text: str) -> tuple[str, str]:
    uuid_nick = message_text.split()[-1].split('_')[1:]
    uuid = uuid_nick[0]
    nick = '_'.join(uuid_nick[1:])
    return uuid, nick


async def authorize_user(user: AIOgramUser, uuid: str, nick: str) -> None:
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})
        if u.nick: raise AlreadyRegistered()
        await u.authorize(uuid, nick)
        print(u)
        await s.commit()
