# Python модули
from aiogram import Router
from aiogram.types import *
from aiogram.filters import *
from aiogram.fsm.context import FSMContext


# Локальные модули
from utils.filters import ElyBy
from logic import core as logic
from messages import core as ms
from keyboards import core as kb


# Переменные
router = Router(name='core_unreg')
router.message.filter(ElyBy(False))
router.callback_query.filter(ElyBy(False))


# Функции
@router.message(CommandStart())
async def message_start(message: Message, user: User, state: FSMContext):
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
async def message_unreg(message: Message, user: User, state: FSMContext):
    await state.clear()
    ms_login = await message.answer(
        text=ms.start_unreg(user),
        reply_markup=kb.elyby_login
    )
    await message.delete()
    await state.set_data({'start_login_id': ms_login.message_id})
