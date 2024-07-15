from aiogram.types import User as AIOgramUser
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from create_bot import bot, rcon
from database import engine
from database.models import User
from utils.exceptions import AlreadyRegistered
from database.dataclasses import User as UserDC
from messages import core as ms


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


async def check_whitelist(user: AIOgramUser) -> bool:
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})


async def edit_start(user: AIOgramUser, data: dict) -> None:
    start_id = data.get('start_id', None)
    u = await get_user_data(user)
    if start_id:
        try:
            if u.nick:
                if u.whitelisted_till: pr_text = u.whitelisted_till.strftime('%d.%m.%Y')
                else: pr_text = None
                await bot.edit_message_text(
                    chat_id=user.id,
                    message_id=start_id,
                    text=ms.start_logged(u.nick, pr_text)
                )
            else:
                await bot.edit_message_text(
                    chat_id=user.id,
                    message_id=start_id,
                    text=ms.start_unreg(user)
                )
        except Exception as e: print(e)


async def add_to_whitelist(user: AIOgramUser) -> None:
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})
        old_whitelist = await rcon.whitelist.get()
        await rcon.whitelist.add(u.nick)
        return u.nick in old_whitelist

    
async def remove_from_whitelist(user: AIOgramUser) -> None:
    async with AsyncSession(engine) as s:
        u = await s.get(User, {'id': user.id})
        old_whitelist = await rcon.whitelist.get()
        await rcon.whitelist.remove(u.nick)
        return u.nick in old_whitelist
