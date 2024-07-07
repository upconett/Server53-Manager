from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter

from logic import core as logic


class ElyByMessage(Filter):
    def __init__(self, registered: bool = True):
        self.registered = registered

    async def __call__(self, message: Message) -> bool:
        user = message.from_user
        nick = await logic.get_nick(user)
        return self.registered == (nick is not None)


class ElyByCallback(Filter):
    def __init__(self, registered: bool = True):
        self.registered = registered

    async def __call__(self, query: CallbackQuery) -> bool:
        user = query.from_user
        nick = await logic.get_nick(user)
        return self.registered == (nick is not None)
