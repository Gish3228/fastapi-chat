from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


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


class User(UserBasePrivate, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)


class UserUpdate(SQLModel):
    name: str | None = None
    login: str | None = None
    password: str | None = None
    info: str | None = None

