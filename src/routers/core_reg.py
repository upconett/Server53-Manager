from aiogram import Router
from aiogram.types import *
from aiogram.filters import *

from create_bot import bot
from logic import core as logic
from utils.filters import ElyByCallback, ElyByMessage

router = Router(name='core_reg')
router.message.filter(ElyByMessage(True))
router.callback_query.filter(ElyByCallback(True))


async def message_start(message: Message):
    user = message.from_user
    await logic.update_user(user)
    


router.message.register(message_start, CommandStart())