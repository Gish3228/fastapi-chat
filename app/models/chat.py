from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class Chat(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str