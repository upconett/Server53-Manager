# Python модули
from aiogram import Router, F
from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter


# Локальные модули
from create_bot import bot
from utils.filters import ElyByMessage
from logic import images as logic
from messages import images as ms
from keyboards import images as kb


# Переменные
router = Router(name='images')
router.message.filter(ElyByMessage(True))


# Классы
class St(StatesGroup):
    rememb_image = State()
    naming_image = State()    
    

# Функции
@router.message(F.caption, (F.photo | F.document))
async def on_image_with_name(message: Message, state: FSMContext) -> None:
    """
    Ловит изображение сразу с подписью.
    :param message: Сообщение Telegram
    :param state: Состояние FSM машины
    """
    print('on_image_with_name')
    if message.photo or 'image' in message.document.mime_type:
        if message.photo:
            file_id = message.photo[-1].file_id
        else:
            file_id = message.document.file_id

        await message.answer(
            text=ms.image_with_name(message.caption),
            reply_markup=kb.image_with_name(message.caption),
            parse_mode='MarkdownV2'
        )

        await state.set_data({
            'file_id': file_id,
            'photo_id': message.message_id
        })
        await state.set_state(St.rememb_image)


@router.message(F.photo | F.document)
async def on_image(message: Message, state: FSMContext) -> None:
    """
    Ловит изображение без подписи.
    :param message: Сообщение Telegram
    :param state: Состояние FSM машины
    """
    print('on_image')
    if message.photo or 'image' in message.document.mime_type:
        if message.photo:
            file_id = message.photo[-1].file_id
        else:
            file_id = message.document.file_id

        await message.answer(
            text=ms.image_no_name,
            reply_markup=kb.image_no_name()
        )

        await state.set_data({
            'file_id': file_id,
            'photo_id': message.message_id
        })
        await state.set_state(St.rememb_image)


@router.callback_query(StateFilter(St.rememb_image), F.data.startswith('image_noname'))
async def start_naming(query: CallbackQuery, state: FSMContext) -> None:
    """
    Начинает процесс именования изображения.
    :param query: Данные inline кнопки
    :param state: Состояние FSM машины
    """
    print('start_naming')
    to_edit = await query.message.edit_text(
        text=ms.image_naming,
        reply_markup=kb.cancel
    )

    data = await state.get_data()
    data['to_edit_id'] = to_edit.message_id

    await state.set_data(data)
    await state.set_state(St.naming_image)


@router.message(StateFilter(St.naming_image), F.text)
async def on_name(message: Message, state: FSMContext):
    """
    Ловит имя изображения.
    :param message: Сообщение Telegram
    :param state: Состояние FSM машины
    """
    print('on_name')
    user = message.from_user
    name = message.text.strip()

    if name.count(' ') > 0:
        await message.answer(ms.no_space)
        await message.delete()
        return

    if not (await logic.unique_name(name)):
        await message.answer(ms.not_unique)
        await message.delete()
        return

    data = await state.get_data()

    await bot.edit_message_text(
        chat_id=user.id,
        message_id=data['to_edit_id'],
        text=ms.image_with_name(name),
        reply_markup=kb.image_with_name(name),
        parse_mode='MarkdownV2'
    )

    await message.delete()
    await state.set_state(St.rememb_image)


@router.callback_query(StateFilter(St.rememb_image), F.data.startswith('image_'))
async def accept_image(query: CallbackQuery, state: FSMContext):
    """
    Принимает подтверждение на загрузку изображения с именем.
    :param query: Данные inline кнопки
    :param state: Состояние FSM машины
    """
    print('accept_image')
    user = query.from_user
    name = logic.extract_name(query.data)
    data = await state.get_data()

    if name.count(' ') > 0:
        await query.answer(text=ms.no_space, show_alert=True)
        return

    if not (await logic.unique_name(name)):
        await query.answer(text=ms.not_unique, show_alert=True)
        return

    await logic.save_image(user, name, data['file_id'])

    await query.message.edit_text(
        text=ms.image_success(name),
        parse_mode='MarkdownV2'
    )

    await state.clear()


@router.callback_query(F.data == 'cancel')
async def on_cancel(query: CallbackQuery, state: FSMContext):
    """
    Отменяет процесс добавления изображения.
    :param query: Данные inline кнопки
    :param state: Состояние FSM машины
    """
    print('on_cancel')
    data = await state.get_data()
    await query.message.delete()
    await bot.delete_message(
        chat_id=query.from_user.id,
        message_id=data['photo_id']
    )
    await state.clear()
