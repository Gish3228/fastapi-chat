from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from uuid import UUID
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .user import User
    from .chat import Chat


class ChatMember(AsyncAttrs, SQLModel, table=True):
    user_id: UUID = Field(index=True, foreign_key='user.id', primary_key=True, ondelete='CASCADE')
    chat_id: UUID = Field(index=True, foreign_key='chat.id', primary_key=True, ondelete='CASCADE')
    role: str

    user: list['User'] = Relationship(back_populates='chat_links')
    chat: list['Chat'] = Relationship(back_populates='user_links')
    
