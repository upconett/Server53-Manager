# Python модули
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from aiomcrcon import Client

import asyncio
import logging


# Локальные модули
from database import engine
from database.models import User
from messages import core as ms


# Классы
class AccessChecker:
    """
    Проверка наличия проходки.
    """
    bot: Bot
    rcon: Client
    frequency: int
    started: bool

    __task: asyncio.Task

    def __init__(self, bot: Bot, rcon: Client, frequency: int):
        self.bot = bot
        self.rcon = rcon
        self.frequency = frequency
        self.started = False

    async def __send_warning(self, user_id: int) -> None:
        """
        Отправка предупреждения пользователю об окончании его проходки.
        """
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=ms.access_warning
            )
        except Exception as e:
            logging.info("Can't send warning:", e)

    async def __check_access(self) -> None:
        """
        Проверка периода действия проходки.
        """
        while self.started:
            async with AsyncSession(engine) as s:
                users = (await s.execute(select(User))).all()
                for u in users:
                    u: User = u[0]
                    if u.access and u.access.whitelisted_till < datetime.now():
                        u.access = None
                        await self.rcon.send_cmd(f'whitelist remove {u.nick}')
                        await self.__send_warning(u.id)
                await s.commit()
            await asyncio.sleep(self.frequency * 3600)

    def start(self) -> None:
        """
        Старт проверки срока действия всех проходок.
        """
        logging.info('Starting AccessChecker...')
        self.started = True
        self.__task = asyncio.create_task(self.__check_access())

    def stop(self) -> None:
        """
        Выключение проверки срока действия всех проходок.
        """
        logging.info('Stopping AccessChecker...')
        self.started = False
        self.__task.cancel()
