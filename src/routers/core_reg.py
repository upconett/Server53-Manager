# Python модули
from aiogram import Router, F
from aiogram.types import *
from aiogram.filters import *
from aiogram.fsm.context import FSMContext


# Локальные модули
from create_bot import bot
import const
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
async def message_start(message: Message, user: User, state: FSMContext):
    data = await state.get_data()

    u = await logic.get_user_data(user)

    if u.access:
        pr_text = u.access.whitelisted_till.strftime('%d.%m.%Y')
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
async def message_imagemaps(message: Message):
    await message.answer(
        text=ms.about_imagemaps,
        reply_markup=kb.back
    )
    await message.delete()


@router.message(StateFilter(None), F.text == 'Инфо ℹ️')
async def message_about_us(message: Message):
    await message.answer(
        text=ms.about_us,
        reply_markup=about_kb.main('about_main')
    )
    await message.delete()


@router.message(StateFilter(None), F.text == 'Подержи 🍺')
async def message_hold_beer(message: Message, state: FSMContext):
    data = await state.get_data()

    to_edit = await message.answer(
        text=ms.donation,
        reply_markup=await kb.donation()
    )

    data['donation_to_edit'] = to_edit.message_id
    await state.set_data(data)
    await message.delete()


@router.message(StateFilter(None), F.text == 'Проходка 🗝️')
async def message_access(message: Message, user: User, state: FSMContext):
    data = await state.get_data()
    u = await logic.get_user_data(user)

    to_edit = await message.answer(
        text=ms.access(u.access),
        reply_markup=await kb.access()
    )
    data['access_to_edit'] = to_edit.message_id
    await state.set_data(data)
    await message.delete()


@router.callback_query(F.data == 'back')
async def query_back(query: CallbackQuery):
    await query.message.delete()


@router.message(Command('leave'))
async def command_leave(message: Message):
    await message.answer(
        text=ms.leave_1,
        reply_markup=kb.leave
    )
    await message.delete()


@router.callback_query(F.data == 'leave')
async def query_leave(query: CallbackQuery, user: User, state: FSMContext):
    await logic.leave_user(user)
    ms_login = await query.message.edit_text(
        text=ms.start_unreg(user),
        reply_markup=kb.elyby_login
    )
    await state.set_data({'start_login_id': ms_login.message_id})


@router.message(F.text.lower().in_(('даешь проходку', 'даёшь проходку')))
async def kicking(message: Message):
    for creator_id in const.creator_ids:
        try:
            await bot.send_message(
                chat_id=creator_id,
                text=f'<b>Игроки</b> <i>хотят</i> <s>чтобы</s> <b><i>вы</i></b> <u>сделали</u> <code>сохранение</code> <a href="https://www.google.com/search?q=Иди+читай+Документацию">проходки</a> 😤'
            )
        except:
            pass
        