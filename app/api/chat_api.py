from fastapi import APIRouter, Depends, status, Body, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from typing import Annotated
from uuid import UUID
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from sqlalchemy.exc import IntegrityError

from ..models.user import User, UserPublicTrunc
from ..models.chat import Chat, ChatCreate, ChatPublic
from ..models.chat_member import ChatMember
from ..dependencies.common import get_session
from ..dependencies.security import GetCurrentUserFactory, check_chat_availability


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


@router.post('/{chat_id}/add_users',
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(check_chat_availability)])
async def add_chat_users(chat_id: UUID,
                         user_ids: Annotated[list[UUID], Body()],
                         session: Annotated[AsyncSession, Depends(get_session)]):

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


@router.get('/{chat_id}/members',
            response_model=list[UserPublicTrunc],
            dependencies=[Depends(check_chat_availability)])
async def get_chat_members(chat_id: UUID,
                           session: Annotated[AsyncSession, Depends(get_session)]):
    chat_data = await session.get(Chat, chat_id, options=[joinedload(Chat.users)])
    return chat_data.users

