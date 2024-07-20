# Python модули
from aiogram.types import User as AIOgramUser
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


# Локальные модули
from create_bot import bot, rcon
from database import engine
from database.models import User
from utils.exceptions import AlreadyRegistered
from database.dataclasses import User as UserDC
from minecraft import MCRcon


# Функции
async def update_user(user: AIOgramUser) -> None:
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})

        if u is None:
            s.add(User(user))
        else:
            await u.update(user)

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


async def get_user_data(user: AIOgramUser) -> UserDC | None:
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})
        if not u:
            return None
        return UserDC(u)


def extract_uuid_nick(message_text: str) -> tuple[str, str]:
    uuid_nick = message_text.split()[-1].split('_')[1:]
    uuid = uuid_nick[0]
    nick = '_'.join(uuid_nick[1:])
    return uuid, nick


async def authorize_user(user: AIOgramUser, uuid: str, nick: str) -> None:
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})
        if u.nick:
            raise AlreadyRegistered()
        await u.authorize(uuid, nick)
        await s.commit()

    
async def leave_user(user: AIOgramUser) -> None:
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})
        if not u.nick: return
        await u.leave()
        await s.commit()


async def add_to_whitelist(user: AIOgramUser) -> bool:
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})
        old_whitelist = await MCRcon.whitelist_get(rcon)
        await rcon.send_cmd(f'whitelist add {u.nick}')
        return u.nick in old_whitelist
