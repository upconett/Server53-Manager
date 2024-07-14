from aiogram import Router, F
from aiogram.types import *
from aiogram.filters import *
from aiogram.fsm.context import FSMContext

from create_bot import bot
from logic import core as logic
from messages import core as ms
from keyboards import core as kb
from utils.filters import ElyByCallback, ElyByMessage

router = Router(name='core_reg')
router.message.filter(ElyByMessage(True))
router.callback_query.filter(ElyByCallback(True))


@router.message(CommandStart())
async def message_start(message: Message, state: FSMContext):
    user = message.from_user
    await logic.update_user(user)
    data = await state.get_data()

    u = await logic.get_user_data(user)
    to_del = await message.answer(
            text=ms.start_logged(u.nick),
            reply_markup=kb.main_menu,
            parse_mode='MarkdownV2'
        )
    await message.delete()
    await logic.delete_extra(user, data)

    data['to_del_start_id'] = to_del.message_id
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


@router.message(StateFilter(None), F.text == 'О нас ⚒️')
async def message_about_us(message: Message, state: FSMContext):
    user = message.from_user
    await logic.update_user(user)

    await message.answer(
        text=ms.about_us,
        reply_markup=kb.back
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


@router.callback_query(F.data == 'back')
async def query_back(query: CallbackQuery):
    user = query.from_user
    await logic.update_user(user)

    await query.message.delete()
