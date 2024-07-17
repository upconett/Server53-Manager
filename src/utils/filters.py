from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter

from logic import core as logic
from logic import admin as logic_admin


# class ElyByMessage(Filter):
#     def __init__(self, registered: bool = True):
#         self.registered = registered

#     async def __call__(self, message: Message) -> bool:
#         user = message.from_user
#         u = await logic.get_user_data(user)
#         return self.registered == ((u.nick if u else u) is not None)


class ElyBy(Filter):
    def __init__(self, registered: bool = True):
        self.registered = registered

    async def __call__(self, event: Message |CallbackQuery) -> bool:
        user = event.from_user
        u = await logic.get_user_data(user)
        return self.registered == ((u.nick if u else u) is not None)


class IsAdmin(Filter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = event.from_user
        admins = await logic_admin.read_admins()
        return user.id in admins
