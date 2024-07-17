from aiogram import Router, F
from aiogram.types import *
from aiogram.filters import *
from aiogram.fsm.context import FSMContext


router = Router(name='admin')
router.message.filter()


@router.message(CommandStart())
async def message_start(message: Message, state: FSMContext):
    pass
