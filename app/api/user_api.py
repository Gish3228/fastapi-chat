from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from psycopg.errors import UniqueViolation, NotNullViolation
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from uuid import UUID

from ..models.user import UserCreate, User, UserPrivate, UserUpdate, UserPublic, UserPublicTrunc
from ..dependencies.common import get_session
from ..dependencies.security import GetCurrentUserFactory
from ..utils.security import get_password_hash
from ..exeptions import login_in_use_exc, not_null_violation_exc, user_not_found_exc


router = APIRouter(tags=['users'])


@router.post('/', status_code=status.HTTP_201_CREATED)
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


@router.get('/', response_model=list[UserPublicTrunc])
async def get_users(session: Annotated[AsyncSession, Depends(get_session)]):
    return (await session.exec(select(User))).all()


@router.get('/me', response_model=UserPrivate)
async def get_users_me(user: Annotated[User, Depends(GetCurrentUserFactory())]):
    return user


@router.patch('/me')
async def update_users_me(user_db: Annotated[User, Depends(GetCurrentUserFactory())],
                          session: Annotated[AsyncSession, Depends(get_session)],
                          user_update: UserUpdate):

    update_data = user_update.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in update_data:
        password = update_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    user_db.sqlmodel_update(update_data, update=extra_data)
    session.add(user_db)
    try:
        await session.commit()
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise login_in_use_exc
        elif isinstance(e.orig, NotNullViolation):
            raise not_null_violation_exc
        else:
            raise
    return {'status': 'ok'}

@router.get('/{user_id}', response_model=UserPublic)
async def get_user(user_id: UUID,
                   session: Annotated[AsyncSession, Depends(get_session)]):
    user = await session.get(User, user_id)
    if not user:
        raise user_not_found_exc
    return user
