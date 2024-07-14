from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import LabeledPrice
from aiogram.methods.create_invoice_link import CreateInvoiceLink

from create_bot import bot
from const import elyby_url


elyby_login = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ElyBy', url=elyby_url, callback_data='login')]
])


main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ImageMaps 🌄')],
    [KeyboardButton(text='О нас ⚒️')],
    [KeyboardButton(text='Подержи 🍺')],
], resize_keyboard=True)


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
    kb.button(text='Поддержать | 25 ⭐', url=await invoice(1))
    kb.button(text='Вернуться', callback_data='back')
    kb.adjust(1, repeat=True)
    return kb.as_markup()
    

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться', callback_data='back')]
])