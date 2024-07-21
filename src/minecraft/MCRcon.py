# Python модули
from aiomcrcon import RCONConnectionError, ClientNotConnectedError, Client
from aiogram.types import Message


# Функции
async def check_mcrcon(rcon: Client, message: Message | None = None):
    try:
        await rcon.send_cmd("checkconnection")
        return True
    except:
        print("Подключение к mcrcon было разорвано.")
        try:
            await rcon.connect()
            print("Подключение к mcrcon установлено.")
            return True
        except Exception as e:
            print(f"Ошибка подключения к mcrcon: {e}")
            if message:
                await message.answer(text='Проблема подключения к серверу, напишите @SteePT и @ppljc!')
            return False


async def whitelist_get(rcon) -> list:
    """
    Возвращает отформатированный вайтлист с сервера.
    """
    response = (await rcon.send_cmd('whitelist list'))[0]
    whitelist = ': '.join(response.replace('\n', '').split(': ')[1:])
    return whitelist.split(', ')
