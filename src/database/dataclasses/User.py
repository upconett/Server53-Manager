# Python модули
from dataclasses import dataclass
from datetime import datetime


# Локальные модули
from database.models import User as UserDB
from database.models import Access as AccessDB


@dataclass
class Access:
    id: int
    nick: str
    whitelisted_till: datetime

    def __init__(self, access: AccessDB | None):
        self.id = access.id
        self.nick = access.nick
        self.whitelisted_till = access.whitelisted_till


@dataclass
class User:
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    
    uuid: str | None
    nick: str | None

    access: Access

    def __init__(self, user: UserDB):
        self.id = user.id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.username = user.username

        self.uuid = user.uuid
        self.nick = user.nick

        self.access = Access(user.access) if user.access else None
