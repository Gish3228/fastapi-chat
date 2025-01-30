from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    login: str = Field(unique=True, index=True)
    password: str
    name: str
    info: str = Field(default='')
    is_active: bool = Field(default=True)


class Chat(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str


class ChatMember(SQLModel, table=True):
    user_id: UUID = Field(index=True, foreign_key='user.id', ondelete='CASCADE')
    chat_id: UUID = Field(index=True, foreign_key='chat.id', ondelete='CASCADE')
    role: str


class Message():
    id: int | None = Field(primary_key=True)
    text: str
    send_time: datetime = Field(default_factory=datetime.now(timezone.utc))
    user_id: UUID = Field(index=True, foreign_key='user.id', ondelete='CASCADE')
    chat_id: UUID = Field(index=True, foreign_key='chat.id', ondelete='CASCADE')

