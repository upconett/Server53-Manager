from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from aiogram.types import User as AIOgramUser
from datetime import datetime, timedelta

from .BaseModel import BaseModel
from .Access import Access


class User(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(unique=True, primary_key=True)

    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]

    uuid: Mapped[str | None]
    nick: Mapped[str | None]

    access: Mapped[Access] = relationship(
        cascade='all, delete-orphan', lazy='selectin'
    )

    # Позволено ли человеку пользоваться ботом
    allowed: Mapped[bool] = mapped_column(default=True)

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

    async def authorize(self, uuid: str, nick: str) -> None:
        self.uuid = uuid
        self.nick = nick

    async def leave(self) -> None:
        self.uuid = None
        self.nick = None

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, nick={self.nick!r})"
