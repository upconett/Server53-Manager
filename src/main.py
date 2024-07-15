import asyncio

from create_bot import bot, dp, rcon
from utils import AccessChecker
from routers import core_unreg, core_reg, images, access, donation
from database import base as db


ac = AccessChecker(frequency=4) # Бот будет проверять проходку каждые 4 часа


async def onstartup():
    await db.check_tables()
    bot_user = await bot.get_me()
    ac.start()
    print(f'{bot_user.full_name} [@{bot_user.username}] up and running | 🌄')


async def onshutdown():
    ac.stop()
    print('Shutting down... | 💤')


async def main():
    dp.startup.register(onstartup)
    dp.shutdown.register(onshutdown)

    try: await rcon.client.connect(); await rcon.client.close()
    except: print("Minecraft RCON connection failed, check .env")

    dp.include_routers(
        core_unreg,
        core_reg,
        images,
        access,
        donation
    )


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try: asyncio.run(main())
    except KeyboardInterrupt: asyncio.run(bot.session.close())

