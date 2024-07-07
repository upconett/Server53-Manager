from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

import config


def_props = DefaultBotProperties(
    parse_mode='HTML'
)

bot = Bot(
    token=config.TOKEN, 
    default=def_props
)
dp = Dispatcher(
    storage=MemoryStorage()
)
