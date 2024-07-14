from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter

from logic import core as logic


class ElyByMessage(Filter):
    def __init__(self, registered: bool = True):
        self.registered = registered

    async def __call__(self, message: Message) -> bool:
        user = message.from_user
        u = await logic.get_user_data(user)
        return self.registered == ((u.nick if u else u) is not None)


class ElyByCallback(Filter):
    def __init__(self, registered: bool = True):
        self.registered = registered

    async def __call__(self, query: CallbackQuery) -> bool:
        user = query.from_user
        u = await logic.get_user_data(user)
        return self.registered == ((u.nick if u else u) is not None)
