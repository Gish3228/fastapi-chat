from sqlmodel import SQLModel, Field
from uuid import UUID
from datetime import datetime, timezone


class Message(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    text: str
    send_time: datetime = Field(default_factory=lambda :datetime.now(timezone.utc))
    user_id: UUID = Field(index=True, foreign_key='user.id', ondelete='CASCADE')
    chat_id: UUID = Field(index=True, foreign_key='chat.id', ondelete='CASCADE')