# Python модули
from aiogram.types import User
from datetime import datetime

# Локальные модули
from config import BOT_USERNAME


# Простые тексты
about_imagemaps = (
	'<b>ImageMaps 🌄</b>\n\n'
	'Вы можете загрузить любую картинку прямо на сервер!\n\n'
	f'Просто отправьте <a href="https://t.me/{BOT_USERNAME}">боту</a> изображение 📩\n\n'
	'А уже в игре используйте команду:\n<code>/imagemaps [название]</code>\nИ кликните на любой блок'
)

about_us = (
	'<b>О нас ⚒️</b>\n\n'
	'Это бот-менеджер Minecraft сервера <u><b>Server53</b></u> 🍃\n\n'
	'<blockquote>Мы лишь хотим создать маленький ламповый сервер и хорошо провести время</blockquote>\n\n'
	'<b>Создатели: @SteePT и @ppljc</b>'
)

donation = (
	'<b>Подержи пиво 🍺</b>\n\n'
	'<s>Да, там опечатка</s> 🤓\n'
	'Но если у вас есть желание поддержать проект, вы можете сделать это тут!'
)


access_warning = (
	'<b>Ваша проходка закончилась 🔒</b>\n\n'
	'Вы не сможете зайти на сервер пока не обновите её 🤕'
)


# Конфигурируемые тексты
def start_unreg(user: User) -> str:
	return (
		"<b>Авторизация 🍞</b>\n\n"
		f"Привет, {user.first_name}!\n"
		"Это бот-менеджер <u><b>Server53</b></u>\n\n"
		"Для начала авторизуйся 🌄\n\n"
		"Ely,by - основа нашего сервера 🏠"
	)


def start_logged(nick: str, pr_text: str | None) -> str:
	pr = f'Проходка до {pr_text} 🗝️' if pr_text else 'Но нужна проходка 🔒'
	return (
		f'<b>С возвращением, {nick} 😄</b>\n\n'
		'Адрес сервера всё тот же:\n'
		'<code>mc.server53.ru</code>\n\n'
		f'{pr}'
	)


def access(whitelisted_till: datetime | None) -> str:
	payd = f'Вы оплатили проходку до {whitelisted_till.strftime("%d.%m.%Y")} 🔓' if whitelisted_till else 'Вы не оплачивали проходку 🔒'
	return (
		'<b>Проходка 🗝️</b>\n\n'
		f'{payd}\n\n'
		'Серверу нужно на что-то жить и чем-то питаться (⚡)'
	)
