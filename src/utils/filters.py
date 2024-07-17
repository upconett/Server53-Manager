# Python модули
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter


# Локальные модули
from logic import core as logic


# Класс
class ElyByMessage(Filter):
    """
    Фильтр, который проверяет, зарегистрирован ли пользователь на Ely.by.
    """
    def __init__(self, registered: bool = True):
        self.registered = registered

    async def __call__(self, message: Message) -> bool:
        user = message.from_user
        u = await logic.get_user_data(user)
        return self.registered == ((u.nick if u else u) is not None)


class ElyByCallback(Filter):
    """
    Фильтр, который проверяет, зарегистрирован ли пользователь на Ely.by.
    """
    def __init__(self, registered: bool = True):
        self.registered = registered

    async def __call__(self, query: CallbackQuery) -> bool:
        user = query.from_user
        u = await logic.get_user_data(user)
        return self.registered == ((u.nick if u else u) is not None)
