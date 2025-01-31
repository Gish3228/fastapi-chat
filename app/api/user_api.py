from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from ..models.user import UserCreate, User
from ..dependencies import get_session
from ..utils import get_password_hash


router = APIRouter(tags=['users'])


@router.post('/')
async def user_post(user: UserCreate, session: Session = Depends(get_session)):
    hashed_password = get_password_hash(user.password)
    db_user = User.model_validate(user, update={'hashed_password': hashed_password})
    session.add(db_user)
    try:
        session.commit()
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=400, detail='Login is already in use')
        else:
            raise
    return {'status': 'ok'}

