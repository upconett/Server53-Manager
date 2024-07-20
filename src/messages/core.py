# Python модули
from aiogram.types import User
from datetime import datetime

# Локальные модули
from config import BOT_USERNAME
from database.dataclasses import Access as AccessDC


# Простые тексты
about_imagemaps = (
	'<b>ImageMaps 🌄</b>\n\n'
	'Вы можете загрузить любую картинку прямо на сервер!\n\n'
	f'Просто отправьте <a href="https://t.me/{BOT_USERNAME}">боту</a> изображение 📩\n\n'
	'А уже в игре используйте команду:\n<code>/imagemap place [название]</code>\nИ кликните на любой блок'
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


leave_1 = (
	'<b>Выход из Ely.by 🚪</b>\n\n'
	'Вы собираетесь выйти из аккаунта?\n'
	'Учтите что проходка привязывается к нику Ely.by, поэтому вы <u>не сможете перенести</u> её между аккаунтами!\n\n'
	'<blockquote>Возможность поменять ник с сохранением проходки скорее всего появится в будущем\n\nОтправьте <b><u>даешь проходку</u></b> чтобы пнуть разрабов 💢</blockquote>'
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
		f'{pr}\n\n'
		'Версия: <b>Forge 1.20.1</b>\n\n'
		'<a href="https://ely.by/load"><b>Установить лаунчер 🕋</b></a>\n'
		'<a href="https://drive.google.com/drive/folders/1FeAl_gZMba6EOyipk3RIBqmJjLEiP9Db"><b>Установить моды 🍱</b></a>'
	)


def access(access: AccessDC | None) -> str:
	payd = f'Вы оплатили проходку до {access.whitelisted_till.strftime("%d.%m.%Y")} 🔓' if access else 'Вы не оплачивали проходку 🔒'
	return (
		'<b>Проходка 🗝️</b>\n\n'
		f'{payd}\n\n'
		'Серверу нужно на что-то жить и чем-то питаться (⚡)'
	)
