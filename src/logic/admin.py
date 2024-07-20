# Python модули
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import MessageEntity
from aiogram.types import User as AIOgramUser

import aiofiles


# Локальные модули
from create_bot import rcon
from database import engine
from database.models import User, Access
from database.dataclasses import User as UserDC
from utils.exceptions import NoUserWithNick, IsSuperAdmin


# Функции
async def get_user_by_nick(nick: str) -> UserDC:
    async with AsyncSession(engine) as s:
        res = (await s.execute(select(User).where(User.nick == nick))).all()
        if len(res) == 0:
            raise NoUserWithNick()
        u = res[0][0]
        return UserDC(u)


async def write_admins(admins: list[int], is_super: bool = False) -> None:
    file = 'super_admins.txt' if is_super else 'admins.txt'
    async with aiofiles.open(file, 'w') as f:
        await f.write('\n'.join(map(str, admins)))


async def read_admins(is_super: bool = False) -> list | None:
    file = 'super_admins.txt' if is_super else 'admins.txt'
    try:
        async with aiofiles.open(file, 'r') as f:
            admins = list(map(int, await f.readlines()))
    except FileNotFoundError:
        await write_admins(admins=[''], is_super=is_super)
        admins = []
    return admins


async def add_admin(nick: str, is_super: bool = False) -> None:
    admins = await read_admins(is_super)
    u = await get_user_by_nick(nick)
    if u.id in admins:
        return

    admins.append(u.id)
    await write_admins(admins, is_super)


async def remove_admin(nick: str) -> bool:
    admins = await read_admins()
    supers = await read_admins(is_super=True)
    u = await get_user_by_nick(nick)

    if u.id in supers:
        return False
    if u.id not in admins:
        return True

    admins.remove(u.id)
    await write_admins(admins)
    return True


async def is_admin(user_id: int, is_super: bool = False) -> bool:
    admins = await read_admins(is_super=is_super)
    return user_id in admins


async def get_players(online: bool = False) -> list[UserDC]:
    result = []
    async with AsyncSession(engine) as s:
        if online:
            players = await rcon.send_cmd('list')
            for p in players:
                u = await s.execute(select(User).where(User.nick == p))
                if len(u.all()) == 0:
                    continue
                result.append(UserDC(u.all()[0][0]))
        else:
            players = await s.execute(select(User))
            result = [UserDC(u[0]) for u in players.all()]
    return result


def sort_users_by_icon(users: list[str]) -> list[str]:
    def sort_key(user):
        if user.startswith("👑"):
            return 0
        elif user.startswith("🛠️"):
            return 1
        else:
            return 2
    return sorted(users, key=sort_key)


async def give_access(nick: str) -> bool:
    result = False
    async with AsyncSession(engine) as s:
        res = (await s.execute(select(User).where(User.nick == nick))).all()
        if len(res) == 0:
            raise NoUserWithNick()
        u: User = res[0][0]
        if u.access:
            await u.access.add_time(1)
            result = True
        else:
            u.access = Access()
            result = False
        await s.commit()
    await rcon.send_cmd(f'whitelist add {nick}')
    return result
        

async def remove_access(nick: str) -> None:
    async with AsyncSession(engine) as s:
        res = (await s.execute(select(User).where(User.nick == nick))).all()
        if len(res) == 0:
            raise NoUserWithNick()
        u: User = res[0][0]
        u.access = None
        await s.commit()
    await rcon.send_cmd(f'whitelist remove {nick}')
        

async def is_user(nick: str) -> bool:
    async with AsyncSession(engine) as s:
        res = (await s.execute(select(User).where(User.nick == nick))).all()
        return len(res) != 0

    
async def block_user(nick: str) -> None:
    async with AsyncSession(engine) as s:
        res = (await s.execute(select(User).where(User.nick == nick))).all()
        if len(res) == 0:
            raise NoUserWithNick()
        u: User = res[0][0]
        if await is_admin(u.id, is_super=True):
            raise IsSuperAdmin()
        u.allowed = False
        await s.commit()


async def unblock_user(nick: str) -> None:
    async with AsyncSession(engine) as s:
        res = (await s.execute(select(User).where(User.nick == nick))).all()
        if len(res) == 0:
            raise NoUserWithNick()
        u: User = res[0][0]
        u.allowed = True
        await s.commit()


async def generate_ms_ent_online(online_list: list[UserDC]) -> tuple[str, list[MessageEntity]]:
    message = 'Игроки онлайн 🕹️\n\n'
    entities = []
    offset = len(message)+2
    for p in online_list:
        if p.nick is None:
            continue
        is_a = await is_admin(p.id)
        is_s = await is_admin(p.id, is_super=True)
        icon = '👑' if is_s else '🛠️' if is_a else '👤'
        name = p.username if p.username else p.first_name
        record = f'{icon} {p.nick} - {name}\n'
        message += record
        entities.append(MessageEntity(
            type='text_mention',
            offset=(offset+len(icon)+len(p.nick)+4),
            length=len(name),
            user=AIOgramUser(
                id=p.id,
                is_bot=False,
                first_name=p.first_name
            )
        ))
        offset += len(record)
    return message, entities


async def generate_ms_ent_all_players(players_list: list[UserDC]) -> tuple[str, list[MessageEntity]]:
    message = 'Все игроки 👥\n\n'
    entities = []
    offset = len(message)+2
    for p in players_list:
        if p.nick is None:
            continue
        is_a = await is_admin(p.id)
        is_s = await is_admin(p.id, is_super=True)
        icon = '👑' if is_s else '🛠️' if is_a else '👤'
        access = '🔒' if p.access is None else f'🗝️ ({p.access.whitelisted_till.strftime("%d.%m.%Y")})'
        name = p.username if p.username else p.first_name
        record = f'{icon} {p.nick} - {name} {access}\n'
        message += record
        entities.append(MessageEntity(
            type='text_mention',
            offset=(offset+len(icon)+len(p.nick)+4),
            length=len(name),
            user=AIOgramUser(
                id=p.id,
                is_bot=False,
                first_name=p.first_name
            )
        ))
        offset += len(record)
    return message, entities
