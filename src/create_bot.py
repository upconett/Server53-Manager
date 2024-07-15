from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

import config
from minecraft import MCRcon


def_props = DefaultBotProperties(
    parse_mode='HTML'
)

bot = Bot(
    token=config.BOT_TOKEN, 
    default=def_props
)
dp = Dispatcher(
    storage=MemoryStorage()
)

rcon = MCRcon(
    host=config.RCON_HOST,
    port=config.RCON_PORT,
    password=config.RCON_PASSWORD
)
