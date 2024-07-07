from aiogram.types import User


def start_unreg(user: User):
    return (
        f"Привет, {user.first_name}!\n\n"
        "Похоже ты не авторизован\n"
        "На нашем сервере авторизация проходит через сервис <b>ElyBy</b>\n"
        "В нем же ты сможешь выбрать или загрузить скин для игры на сервере!"
    )

