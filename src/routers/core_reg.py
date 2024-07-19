# Python модули
from aiogram import Router, F
from aiogram.types import *
from aiogram.filters import *
from aiogram.fsm.context import FSMContext


# Локальные модули
from logic import core as logic
from messages import core as ms
from keyboards import core as kb
from keyboards import about as about_kb
from utils.filters import ElyBy


# Переменные
router = Router(name='core_reg')
router.message.filter(ElyBy(True))
router.callback_query.filter(ElyBy(True))


# Функции
@router.message(F.text == 'Домой 🏠')
@router.message(Command('start', 'help'))
async def message_start(message: Message, state: FSMContext):
    user = message.from_user
    await logic.update_user(user)
    data = await state.get_data()

    u = await logic.get_user_data(user)

    if u.whitelisted_till:
        pr_text = u.whitelisted_till.strftime('%d.%m.%Y')
    else:
        pr_text = None

    to_del = await message.answer(
            text=ms.start_logged(u.nick, pr_text),
            reply_markup=kb.main_menu
        )

    await message.delete()
    await logic.delete_extra(user, data)

    data['start_id'] = to_del.message_id
    await state.set_data(data)


@router.message(StateFilter(None), F.text == 'ImageMaps 🌄')
async def message_imagemaps(message: Message, state: FSMContext):
    user = message.from_user
    await logic.update_user(user)
    
    await message.answer(
        text=ms.about_imagemaps,
        reply_markup=kb.back
    )
    await message.delete()


@router.message(StateFilter(None), F.text == 'Инфо ℹ️')
async def message_about_us(message: Message, state: FSMContext):
    user = message.from_user
    await logic.update_user(user)

    await message.answer(
        text=ms.about_us,
        reply_markup=about_kb.main('about_main')
    )
    await message.delete()


@router.message(StateFilter(None), F.text == 'Подержи 🍺')
async def message_hold_beer(message: Message, state: FSMContext):
    user = message.from_user
    await logic.update_user(user)

    data = await state.get_data()

    to_edit = await message.answer(
        text=ms.donation,
        reply_markup=await kb.donation()
    )

    data['donation_to_edit'] = to_edit.message_id
    await state.set_data(data)
    await message.delete()


@router.message(StateFilter(None), F.text == 'Проходка 🗝️')
async def message_access(message: Message, state: FSMContext):
    user = message.from_user
    await logic.update_user(user)

    data = await state.get_data()
    u = await logic.get_user_data(user)

    to_edit = await message.answer(
        text=ms.access(u.whitelisted_till),
        reply_markup=await kb.access()
    )
    data['access_to_edit'] = to_edit.message_id
    await state.set_data(data)
    await message.delete()


@router.callback_query(F.data == 'back')
async def query_back(query: CallbackQuery):
    user = query.from_user
    await logic.update_user(user)
    await query.message.delete()
