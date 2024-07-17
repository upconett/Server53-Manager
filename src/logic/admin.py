import aiofiles
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from create_bot import rcon
from database import engine
from database.models import User
from database.dataclasses import User as UserDC
from utils.exceptions import NoUserWithNick, IsSuperAdmin


async def get_user_by_nick(nick: str) -> UserDC:
    async with AsyncSession(engine) as s:
        res = (await s.execute(select(User).where(User.nick == nick))).all()
        if len(res) == 0: raise NoUserWithNick()
        u = res[0][0]
        return UserDC(u)


async def write_admins(admins: list[int], super: bool = False) -> None:
    file = 'super_admins.txt' if super else 'admins.txt'
    async with aiofiles.open(file, 'w') as f:
        await f.write('\n'.join(map(str,admins)))


async def read_admins(super: bool = False) -> list | None:
    file = 'super_admins.txt' if super else 'admins.txt'
    try:
        async with aiofiles.open(file, 'r') as f:
            admins = list(map(int, await f.readlines()))
    except:
        await write_admins([''], super=super)
        admins = []
    return admins


async def add_admin(nick: str, super: bool = False) -> None:
    admins = await read_admins(super)
    u = await get_user_by_nick(nick)
    if u.id in admins: return

    admins.append(u.id)
    await write_admins(admins, super)


async def remove_admin(nick: str) -> bool:
    admins = await read_admins()
    supers = await read_admins(super=True)
    u = await get_user_by_nick(nick)
    if u.id in supers: return False
    if u.id not in admins: return True

    admins.remove(u.id)
    await write_admins(admins)
    return True


async def is_admin(user_id: int, super: bool = False) -> bool:
    admins = await read_admins(super=super)
    return user_id in admins


async def get_players(online: bool = False) -> list[UserDC]:
    result = []
    async with AsyncSession(engine) as s:
        if online:
            players = await rcon.list()
            for p in players:
                u = await s.execute(select(User).where(User.nick == p))
                if len(u.all()) == 0: continue
                result.append(UserDC(u.all()[0][0]))
        else:
            players = await s.execute(select(User))
            result = [UserDC(u[0]) for u in players.all()]
    return result


def sort_users_by_icon(users: list[str]) -> list[str]:
    def sort_key(user):
        if user.startswith("👑"): return 0
        elif user.startswith("🛠️"): return 1
        else: return 2
    return sorted(users, key=sort_key)


async def give_access(nick: str) -> bool:
    async with AsyncSession(engine) as s:
        res = (await s.execute(select(User).where(User.nick == nick))).all()
        if len(res) == 0: raise NoUserWithNick()
        u: User = res[0][0]
        if u.whitelisted_till:
            await u.add_time(1)
            result = 1
        else:
            await u.create_time(1)
            result = 0
        await s.commit()
    await rcon.whitelist.add(nick)
    return result
        

async def remove_access(nick: str) -> None:
    async with AsyncSession(engine) as s:
        res = (await s.execute(select(User).where(User.nick == nick))).all()
        if len(res) == 0: raise NoUserWithNick()
        u: User = res[0][0]
        u.whitelisted_till = None
        await s.commit()
    await rcon.whitelist.remove(nick)
        

async def is_user(nick: str) -> bool:
    async with AsyncSession(engine) as s:
        res = (await s.execute(select(User).where(User.nick == nick))).all()
        return len(res) != 0

    
async def block_user(nick: str) -> None:
    async with AsyncSession(engine) as s:
        res = (await s.execute(select(User).where(User.nick == nick))).all()
        if len(res) == 0: raise NoUserWithNick()
        u: User = res[0][0]
        if await is_admin(u.id, super=True): raise IsSuperAdmin()
        u.allowed = False
        await s.commit()


async def unblock_user(nick: str) -> None:
    async with AsyncSession(engine) as s:
        res = (await s.execute(select(User).where(User.nick == nick))).all()
        if len(res) == 0: raise NoUserWithNick()
        u: User = res[0][0]
        u.allowed = True
        await s.commit()