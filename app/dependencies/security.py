from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlmodel import Session, select
from argon2.exceptions import VerifyMismatchError

from ..models.user import User
from .common import get_session
from ..utils.security import verify_password
from ..exeptions import invalid_credentials_exc
from ..config import settings


async def authenticate_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                            session: Annotated[Session, Depends(get_session)]) -> User:
    user = session.exec(select(User).where(User.login == form_data.username)).first()
    if not user:
        raise invalid_credentials_exc
    try:
        verify_password(user.hashed_password, form_data.password)
    except VerifyMismatchError:
        raise invalid_credentials_exc
    return user

async def get_jwt_settings():
    return settings.jwt
