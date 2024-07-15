from aiogram import Router, F
from aiogram.types import *
from aiogram.filters import *
from aiogram.fsm.context import FSMContext
from typing import List

from create_bot import bot
from utils.filters import ElyByMessage, ElyByCallback

from logic import core as logic
from messages import core as ms
from keyboards import core as kb

router = Router(name='core_unreg')
router.message.filter(ElyByMessage(False))
router.callback_query.filter(ElyByCallback(False))


@router.message(Command('start', 'help'))
async def message_start(message: Message, state: FSMContext):
    user = message.from_user
    await logic.update_user(user)

    data = await state.get_data()
    await logic.delete_extra(user, data)
    await state.clear()

    if 'login_' in message.text:
        try:
            uuid, nick = logic.extract_uuid_nick(message.text)
            await logic.authorize_user(user, uuid, nick)
            await message.answer(
                text=ms.start_logged(nick, None),
                reply_markup=kb.main_menu
            )
            await message.delete()
        except Exception as e:
            print(e)
            ms_login = await message.answer(
                text=ms.start_unreg(user),
                reply_markup=kb.elyby_login
            )
            await state.set_data({'start_login_id': ms_login.message_id})

    else:
        ms_login = await message.answer(
            text=ms.start_unreg(user),
            reply_markup=kb.elyby_login
        )
        await state.set_data({'start_login_id': ms_login.message_id})
        await message.delete()

    
@router.message()
async def message_unreg(message: Message, state: FSMContext):
    user = message.from_user
    await logic.update_user(user)

    data = await state.get_data()
    await state.clear()

    ms_login = await message.answer(
        text=ms.start_unreg(user),
        reply_markup=kb.elyby_login
    )
    await message.delete()
    await state.set_data({'start_login_id': ms_login.message_id})
