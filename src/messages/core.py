from aiogram.types import User

from utils.funcs import escape_mdv2
from config import BOT_USERNAME


def start_unreg(user: User) -> str:
    return (
        f"Привет, {user.first_name}!\n\n"
        "Похоже ты не авторизован\n"
        "На нашем сервере авторизация проходит через сервис <b>ElyBy</b>\n"
        "В нем же ты сможешь выбрать или загрузить скин для игры на сервере!"
    )


def start_logged(nick: str) -> str:
    nick = escape_mdv2(nick)
    return (
        f'*С возвращением, {nick} 😄*\n\n'
        'Адрес сервера всё тот же:\n'
        '`mc.server53.ru`'
    )


about_imagemaps = (
    '<b>ImageMaps 🌄</b>\n'
    'На сервере установлен <b>плагин</b>, позволяющий загружать на сервер <i>любые</i> картинки в виде карт\n\n'
    f'Вы можете загрузить новую картинку, просто отправив <a href="https://t.me/{BOT_USERNAME}">боту</a> изображение 📩\n\n'
    'На сервере используйте команду:\n<code>/imagemaps [название]</code>\nТак вы разместите картину'
)

about_us = (
    '<b>О нас ⚒️</b>\n'
    'Это бот-менеджер <a href="https://ru.wikipedia.org/wiki/Minecraft">Minecraft</a> сервера <u><b>Server53</b></u> 🍃\n'
    'Мы лишь хотим создать маленький ламповый сервер и хорошо провести время\n\n'
    '<b>Создатели: @SteePT и @ppljc</b>'
)

donation = (
    '<b>Подержи пиво 🍺</b>\n\n'
    '<s>Да, там опечатка</s> 🤓\n'
    'Но если у вас есть желание поддержать проект, вы можете сделать это тут!'
)
