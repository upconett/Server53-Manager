from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, func
from aiogram.types import User as AIOgramUser
from datetime import datetime, timedelta

from .BaseModel import BaseModel


class Access(BaseModel):
    """
    Модель проходки на сервер, связана с игроком по нику
    """
    __tablename__ = 'accesses'

    id: Mapped[int] = mapped_column(unique=True, primary_key=True, autoincrement=True)
    nick: Mapped[str] = mapped_column(ForeignKey('users.nick', ondelete='CASCADE'))
    whitelisted_till: Mapped[datetime | None] = mapped_column(default=func.now())

    def __init__(self, months: int = 1):
        super().__init__()
        self.whitelisted_till = datetime.now() + timedelta(days=31*months)

    async def add_time(self, months: int = 1) -> None:
        self.whitelisted_till += timedelta(days=31*months)

    def __repr__(self) -> str:
        return f"Access(id={self.id!r}, nick={self.nick!r}, whitelisted_till={self.whitelisted_till.strftime('%d.%m.%Y')!r})"
