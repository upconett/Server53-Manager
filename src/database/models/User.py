from sqlalchemy.orm import Mapped, mapped_column
from aiogram.types import User as AIOgramUser

from .BaseModel import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(unique=True, primary_key=True)

    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]

    nick: Mapped[str | None]


    def __init__(self, user: AIOgramUser):
        super().__init__()
        self.id = user.id
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name


    async def update(self, user: AIOgramUser) -> None:   
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name


    async def set_nick(self, nick: str) -> None:
        self.nick = nick


    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, nick={self.nick!r})"
    