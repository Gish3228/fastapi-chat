from fastapi import APIRouter, Depends, status, Body, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import joinedload
from typing import Annotated
from uuid import UUID
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from sqlalchemy.exc import IntegrityError

from ..models.user import User
from ..models.chat import Chat, ChatCreate, ChatPublic
from ..models.chat_member import ChatMember
from ..dependencies.common import get_session
from ..dependencies.security import GetCurrentUserFactory, get_current_user_id
from ..exeptions import access_forbidden_exc


router = APIRouter(tags=['chats'])


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_chat(chat: ChatCreate,
                      user: Annotated[User, Depends(GetCurrentUserFactory())],
                      session: Annotated[AsyncSession, Depends(get_session)]):
    db_chat = Chat.model_validate(chat)
    db_chat.user_links = [ChatMember(user=user)]
    session.add(db_chat)
    await session.commit()
    return {'status': 'ok'}


@router.get('/me', response_model=list[ChatPublic])
async def read_user_chats(user: Annotated[User, Depends(GetCurrentUserFactory(joinedload(User.chats)))]):
    return user.chats


@router.post('/{chat_id}/add_users', status_code=status.HTTP_201_CREATED)
async def add_chat_users(chat_id: UUID,
                         user_ids: Annotated[list[UUID], Body()],
                         current_user_id: Annotated[UUID, Depends(get_current_user_id)],
                         session: Annotated[AsyncSession, Depends(get_session)]):
    statement = select(select(ChatMember)
                       .where(ChatMember.user_id == current_user_id)
                       .where(ChatMember.chat_id == chat_id)
                       .exists())
    chat_query = await session.exec(statement)
    if not chat_query.first():
        raise access_forbidden_exc
    
    session.add_all(ChatMember(user_id=user_id, chat_id=chat_id) for user_id in user_ids)
    try:
        await session.commit()
    except IntegrityError as e:
        if isinstance(e.orig, ForeignKeyViolation):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        elif isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User is already in chat')
        else:
            raise
    return {'status': 'ok'}
    

