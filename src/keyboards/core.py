# Python модули
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import LabeledPrice
from aiogram.methods.create_invoice_link import CreateInvoiceLink

# Локальные модули
from create_bot import bot
from const import elyby_url

# Простые клавиатуры
elyby_login = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Авторизоваться в Ely.by', url=elyby_url, callback_data='login')]
])

main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Домой 🏠')],
    [KeyboardButton(text='Проходка 🗝️')],
    [KeyboardButton(text='ImageMaps 🌄')],
    [KeyboardButton(text='Инфо ℹ️'), KeyboardButton(text='Подержи 🍺')],
], resize_keyboard=True)


# Конфигурируемые клавиатуры
async def donation() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    async def invoice(currency: int):
        prices = [LabeledPrice(label="XTR", amount=currency)]
        return await bot(
            CreateInvoiceLink(
                title="Поддержка 🍺",
                description="Поддержи проект Server53",
                prices=prices,
                provider_token="",
                payload="donation",
                currency="XTR",
            )
        )

    kb.button(text='Поддержать | 25 ⭐', url=await invoice(25))
    kb.button(text='Вернуться', callback_data='back')
    kb.adjust(1, repeat=True)
    return kb.as_markup()


async def access() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    async def invoice(currency: int):
        prices = [LabeledPrice(label="XTR", amount=currency)]
        return await bot(
            CreateInvoiceLink(
                title="1 Месяц 🗝️",
                description="Проходка на Server53",
                prices=prices,
                provider_token="",
                payload="1_month_access",
                currency="XTR",
            )
        )

    kb.button(text='1 Месяц | 12 ⭐', url=await invoice(12))
    kb.button(text='Вернуться', callback_data='back')
    kb.adjust(1, repeat=True)
    return kb.as_markup()


back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться', callback_data='back')]
])

leave = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выйти из Ely.by', callback_data='leave')],
    [InlineKeyboardButton(text='Вернуться', callback_data='back')]
])