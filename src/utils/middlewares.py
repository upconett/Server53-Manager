from aiogram import BaseMiddleware
from aiogram.types import *
from typing import *

from logic.core import update_user


class StandartMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user = event.from_user
        data['user'] = user
        await update_user(user)
        return await handler(event, data)
