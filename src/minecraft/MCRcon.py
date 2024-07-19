# Python модули
from aiomcrcon import RCONConnectionError, ClientNotConnectedError

import functools


# Функции
# def check_mcrcon(func):
#     @functools.wraps(func)
#     async def wrapper(rcon, *args, **kwargs):
#         try:
#             await rcon.send_cmd("checkconnection")
#         except ClientNotConnectedError:
#             print("Подключение к mcrcon было разорвано.")
#
#             try:
#                 await rcon.connect()
#
#                 print("Подключение к mcrcon установлено.")
#             except RCONConnectionError as e:
#                 print(f"Ошибка подключения к mcrcon: {e}")
#
#                 return
#
#         return await func(*args, **kwargs)
#     return wrapper


async def check_mcrcon(rcon):
    try:
        await rcon.send_cmd("checkconnection")
    except ClientNotConnectedError:
        print("Подключение к mcrcon было разорвано.")

        try:
            await rcon.connect()

            print("Подключение к mcrcon установлено.")
        except RCONConnectionError as e:
            print(f"Ошибка подключения к mcrcon: {e}")

            return


async def whitelist_get(rcon) -> list:
    """
    Возвращает отформатированный вайтлист с сервера.
    """
    response = (await rcon.send_cmd('whitelist list'))[0]
    whitelist = ': '.join(response.replace('\n', '').split(': ')[1:])
    return whitelist.split(', ')
