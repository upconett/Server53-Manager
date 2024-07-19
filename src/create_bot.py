# Python модули
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage


# Локальные модули
from utils import AccessChecker
from minecraft import rcon

import config


# Основные объекты для взаимодействия
def_props = DefaultBotProperties(
    parse_mode='HTML',
    link_preview_is_disabled=True
)

bot = Bot(
    token=config.BOT_TOKEN, 
    default=def_props
)

dp = Dispatcher(
    storage=MemoryStorage()
)

ac = AccessChecker(
    bot=bot, rcon=rcon,
    frequency=config.ACCESS_CHECK_FREQUENCY
) 
