from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class UserBase(SQLModel):
    login: str = Field(unique=True, index=True)
    name: str
    info: str = Field(default='')


class UserCreate(UserBase):
    password: str


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
