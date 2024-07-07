from aiogram import Router
from aiogram.types import *
from aiogram.filters import *

from create_bot import bot
from utils.filters import ElyByMessage, ElyByCallback

from logic import core as logic
from messages import core as ms
from keyboards import core as kb

router = Router(name='core_unreg')
router.message.filter(ElyByMessage(False))
router.callback_query.filter(ElyByCallback(False))


async def message_start(message: Message):
    user = message.from_user
    await logic.update_user(user)

    await message.answer(
        text=ms.start_unreg(user),
        reply_markup=kb.elyby_login()
    )


router.message.register(message_start, CommandStart())
