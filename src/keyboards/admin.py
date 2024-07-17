from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from const import admin_sections


main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Домой 🏠'), KeyboardButton(text='Панель 🛠️')],
    [KeyboardButton(text='Проходка 🗝️')],
    [KeyboardButton(text='ImageMaps 🌄')],
    [KeyboardButton(text='О нас ⚒️'), KeyboardButton(text='Подержи 🍺')],
], resize_keyboard=True)


def admin_panel(exc: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for s in admin_sections:
        if s == exc: continue
        kb.button(text=admin_sections[s], callback_data=s)
    kb.adjust(2, repeat=True)
    kb.row(InlineKeyboardButton(text='Вернуться', callback_data='back'))
    return kb.as_markup()
