from sqlmodel import SQLModel, Field
from uuid import UUID


class ChatMember(SQLModel, table=True):
    user_id: UUID = Field(index=True, foreign_key='user.id', primary_key=True, ondelete='CASCADE')
    chat_id: UUID = Field(index=True, foreign_key='chat.id', primary_key=True, ondelete='CASCADE')
    role: str
    
