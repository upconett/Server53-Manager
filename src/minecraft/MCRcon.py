# Локальные модули
from create_bot import rcon


# Функции
async def whitelist_get() -> list:
    """
    Возвращает отформатированный вайтлист с сервера.
    """
    response = (await rcon.send_cmd('whitelist list'))[0]
    whitelist = ': '.join(response.replace('\n', '').split(': ')[1:])
    return whitelist.split(', ')
