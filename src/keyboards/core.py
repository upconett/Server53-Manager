from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def elyby_login():
    kb = InlineKeyboardBuilder()
    kb.button(text='ElyBy', url="https://account.ely.by/oauth2/v1?client_id=server53bot&redirect_uri=https://t.me/test_work_upco_bot&response_type=code&scope=account_info")
    return kb.as_markup()
