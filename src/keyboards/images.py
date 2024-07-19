# Python модули
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Простые клавиатуры
cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
])


# Конфигурируемые клавиатуры
def image_no_name() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Добавить', callback_data=fr'image_noname')
    kb.button(text='Отмена', callback_data='cancel')
    kb.adjust(1, repeat=True)
    return kb.as_markup()


def image_with_name(name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Добавить', callback_data=f'image_{name}')
    kb.button(text='Отмена', callback_data=f'cancel')
    kb.adjust(1, repeat=True)
    return kb.as_markup()
    