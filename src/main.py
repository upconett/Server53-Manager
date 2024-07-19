# Python модули
import asyncio
import logging

# Локальные модули
from create_bot import bot, dp, rcon, ac
from routers import admin, core_unreg, core_reg, about, images, access, donation
from database import base as db
from utils.middlewares import StandartMiddleware



# Функции при запуске и выключении бота
async def onstartup():
    await db.check_tables()
    bot_user = await bot.get_me()
    ac.start()
    logging.info(f'{bot_user.full_name} [@{bot_user.username}] up and running | 🌄')


async def onshutdown():
    await rcon.close()
    ac.stop()
    logging.info('Shutting down... | 💤')


# Функция запуска бота
async def main():
    dp.startup.register(onstartup)
    dp.shutdown.register(onshutdown)

    try:
        await rcon.connect()
    except:
        logging.info("Minecraft RCON connection failed, check .env")

    dp.message.middleware(StandartMiddleware())
    dp.callback_query.middleware(StandartMiddleware())
    dp.pre_checkout_query.middleware(StandartMiddleware())

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
