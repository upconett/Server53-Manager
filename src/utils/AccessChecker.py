from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio
from datetime import datetime

from minecraft import MCRcon
from database import engine
from database.models import User
from messages import core as ms


class AccessChecker:

    bot: Bot
    rcon: MCRcon
    frequency: int
    started: bool

    __task: asyncio.Task

    def __init__(self, bot: Bot, rcon: MCRcon, frequency: int): 
        self.bot = bot
        self.rcon = rcon
        self.frequency = frequency
        self.started = False


    async def __send_warning(self, user_id: int) -> None:
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=ms.access_warning
            )
        except Exception as e:
            print("Can't send warning:", e)


    async def __check_access(self):
        while self.started:
            async with AsyncSession(engine) as s:
                users = (await s.execute(select(User))).all()
                for u in users:
                    u: User = u[0]
                    if u.whitelisted_till < datetime.now():
                        u.whitelisted_till = None
                        await self.rcon.whitelist.remove(u.nick)
                        await self.__send_warning(u.id)
                await s.commit()
            await asyncio.sleep(self.frequency * 3600)


    def start(self):
        print('Starting AccessChecker...')
        self.started = True
        self.__task = asyncio.create_task(self.__check_access())
    

    def stop(self):
        print('Stopping AccessChecker...')
        self.started = False
        self.__task.cancel()
