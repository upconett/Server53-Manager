from dataclasses import dataclass
from database.models import User as UserDB


@dataclass
class User:
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    
    uuid: str | None
    nick: str | None

    def __init__(self, user: UserDB):
        self.id = user.id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.username = user.username

        self.uuid = user.uuid
        self.nick = user.nick
