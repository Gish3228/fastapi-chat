from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from uuid import UUID, uuid4
from typing import TYPE_CHECKING
from .chat_member import ChatMember


if TYPE_CHECKING:
    from .user import User
    from .message import Message


class Chat(AsyncAttrs, SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str

    user_links: list[ChatMember] = Relationship(back_populates='chat', passive_deletes=True)
    users: list['User'] = Relationship(back_populates='chats', link_model=ChatMember,
                                       sa_relationship_kwargs={'viewonly': True})
    messages: list['Message'] = Relationship(back_populates='chat', passive_deletes=True)
    