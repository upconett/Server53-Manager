# Python модули
import asyncio

# Локальные модули
from create_bot import bot, dp, rcon, ac
from routers import admin, core_unreg, core_reg, about, images, access, donation
from database import base as db


# Функции при запуске и выключении бота
async def onstartup():
    await db.check_tables()
    bot_user = await bot.get_me()
    ac.start()
    print(f'{bot_user.full_name} [@{bot_user.username}] up and running | 🌄')


async def onshutdown():
    await rcon.close()
    ac.stop()
    print('Shutting down... | 💤')


# Функция запуска бота
async def main():
    dp.startup.register(onstartup)
    dp.shutdown.register(onshutdown)

    try:
        await rcon.connect()
    except:
        print("Minecraft RCON connection failed, check .env")

    dp.include_routers(
        admin,
        core_unreg,
        core_reg,
        about,
        images,
        access,
        donation
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Запуск бота
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.run(bot.session.close())
