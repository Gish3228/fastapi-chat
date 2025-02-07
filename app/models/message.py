from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from uuid import UUID
from datetime import datetime, timezone
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .user import User
    from .chat import Chat


class Message(AsyncAttrs, SQLModel, table=True):
    __tablename__ = 'message'
    
    id: int | None = Field(primary_key=True)
    text: str
    send_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: UUID = Field(index=True, foreign_key='user.id', ondelete='CASCADE')
    chat_id: UUID = Field(index=True, foreign_key='chat.id', ondelete='CASCADE')

    user: list['User'] = Relationship(back_populates='messages')
    chat: list['Chat'] = Relationship(back_populates='messages')
