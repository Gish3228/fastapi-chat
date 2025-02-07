from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from uuid import UUID, uuid4
from typing import TYPE_CHECKING
from .chat_member import ChatMember

if TYPE_CHECKING:
    from .chat import Chat
    from .message import Message


class UserBasePublic(SQLModel):
    name: str
    info: str = Field(default='')


class UserBasePrivate(UserBasePublic):
    login: str = Field(unique=True, index=True)


class UserPublic(UserBasePublic):
    pass

class UserPrivate(UserBasePrivate):
    pass


class UserCreate(UserBasePrivate):
    password: str


class UserUpdate(SQLModel):
    name: str | None = None
    login: str | None = None
    password: str | None = None
    info: str | None = None


class User(AsyncAttrs, UserBasePrivate, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)

    chat_links: list[ChatMember] = Relationship(back_populates='user', passive_deletes=True)
    chats: list['Chat'] = Relationship(back_populates='users', link_model=ChatMember,
                                       sa_relationship_kwargs={'viewonly': True})
    messages: list['Message'] = Relationship(back_populates='user', passive_deletes=True)
