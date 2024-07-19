from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from const import admin_sections


main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Домой 🏠'), KeyboardButton(text='Панель 🛠️')],
    [KeyboardButton(text='Проходка 🗝️')],
    [KeyboardButton(text='ImageMaps 🌄')],
    [KeyboardButton(text='Инфо ℹ️'), KeyboardButton(text='Подержи 🍺')],
], resize_keyboard=True)


def admin_panel(exc: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for s in admin_sections:
        cb_data = 'admin_current' if s == exc else s
        kb.button(text=admin_sections[s], callback_data=cb_data)
    kb.adjust(1, 2, repeat=True)
    kb.row(InlineKeyboardButton(text='Вернуться', callback_data='back'))
    return kb.as_markup()
