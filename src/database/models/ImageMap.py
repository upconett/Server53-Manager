from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from .BaseModel import BaseModel
from database.models import User as UserDB


class ImageMap(BaseModel):
    __tablename__ = 'imagemaps'

    id: Mapped[int] = mapped_column(unique=True, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(unique=True)
    creator: Mapped[int] = mapped_column(ForeignKey('users.id'))


    def __init__(self, name: str, creator: UserDB):
        super().__init__()
        self.name = name
        self.creator = creator.id

    def get_path(self) -> str:
        return self.name + '.png'


    def __repr__(self) -> str:
        return f"ImageMap(id={self.id!r}, name={self.name!r}, creator={self.creator!r})"
    