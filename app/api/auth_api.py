from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from ..models.user import User
from ..models.misc import Token
from ..dependencies.security import authenticate_user, get_jwt_settings
from ..config import JWTSettings
from ..utils.security import create_access_token



router = APIRouter(tags=['auth'])


@router.post('/')
async def login(user: Annotated[User, Depends(authenticate_user)],
                jwt_settings: Annotated[JWTSettings, Depends(get_jwt_settings)]) -> Token:
    access_token = create_access_token(
        data={"sub": str(user.id)}, jwt_settings=jwt_settings
    )
    return Token(access_token=access_token, token_type="bearer")
