# Python модули
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Локальные модули
from const import about_sections


# Функции
def main(exc: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for s in about_sections:
        if s == exc:
            continue
        kb.button(text=about_sections[s], callback_data=s)
    kb.adjust(2, repeat=True)
    kb.row(InlineKeyboardButton(text='Вернуться', callback_data='back'))
    return kb.as_markup()
