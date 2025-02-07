from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from argon2.exceptions import VerifyMismatchError
from jwt.exceptions import InvalidTokenError
from uuid import UUID
import jwt

from ..models.user import User
from ..models.misc import TokenData
from .common import get_session
from ..utils.security import verify_password
from ..exeptions import invalid_credentials_exc, invalid_token_exc
from ..config import settings, JWTSettings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/")


async def authenticate_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                            session: Annotated[AsyncSession, Depends(get_session)]) -> User:
    user_query = await session.exec(select(User).where(User.login == form_data.username))
    user = user_query.first()
    if not user:
        raise invalid_credentials_exc
    try:
        verify_password(user.hashed_password, form_data.password)
    except VerifyMismatchError:
        raise invalid_credentials_exc
    return user


async def get_jwt_settings():
    return settings.jwt


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)], 
                              jwt_settings: Annotated[JWTSettings, Depends(get_jwt_settings)]) -> UUID:
    try:
        payload = jwt.decode(token, jwt_settings.secret_key, algorithms=[jwt_settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise invalid_token_exc
        token_data = TokenData(user_id=user_id)
    except InvalidTokenError:
        raise invalid_token_exc
    return token_data.user_id


class GetCurrentUserFactory:
    def __init__(self, *args):
        self.options = args

    async def __call__(self,
                       user_id: Annotated[UUID, Depends(get_current_user_id)],
                       session: Annotated[AsyncSession, Depends(get_session)]) -> User:
        user = await session.get(User, user_id, options=self.options)
        if user is None:
            raise invalid_token_exc
        return user
    