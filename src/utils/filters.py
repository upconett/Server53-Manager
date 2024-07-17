# Python модули
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter


# Локальные модули
from logic import core as logic
from logic import admin as logic_admin


# Класс
class ElyBy(Filter):
    """
    Фильтр, который проверяет, зарегистрирован ли пользователь в Ely.by.
    """
    def __init__(self, registered: bool = True):
        self.registered = registered

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = event.from_user
        u = await logic.get_user_data(user)
        return self.registered == ((u.nick if u else u) is not None)


# Класс
class IsAdmin(Filter):
    """
    Фильтр, который провяет, является ли пользователь админом или супер-админом.
    """
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = event.from_user
        admins = await logic_admin.read_admins()
        return user.id in admins
