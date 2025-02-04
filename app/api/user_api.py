from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from typing import Annotated

from ..models.user import UserCreate, User
from ..dependencies.common import get_session
from ..utils.security import get_password_hash
from ..exeptions import login_in_use_exc


router = APIRouter(tags=['users'])


@router.post('/')
async def user_post(user: UserCreate, session: Annotated[AsyncSession, Depends(get_session)]):
    hashed_password = get_password_hash(user.password)
    db_user = User.model_validate(user, update={'hashed_password': hashed_password})
    session.add(db_user)
    try:
        await session.commit()
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise login_in_use_exc
        else:
            raise
    return {'status': 'ok'}

