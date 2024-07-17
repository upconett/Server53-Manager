import aiofiles


async def write_admins(admins: list[int]) -> None:
    async with aiofiles.open('admins.txt', 'w') as f:
        await f.write('\n'.join(admins))


async def read_admins() -> list | None:
    try:
        async with aiofiles.open('admins.txt', 'r') as f:
            admins = list(map(int, await f.readlines()))
    except:
        await write_admins([''])
        admins = []
    return admins


async def add_admin(admin_id: int) -> None:
    admins = await read_admins()
    if admin_id in admins: return

    admins.append(admin_id)
    await write_admins(admins)


async def remove_admin(admin_id: int) -> None:
    admins = await read_admins()
    if admin_id not in admins: return

    admins.remove(admin_id)
    await write_admins(admins)
