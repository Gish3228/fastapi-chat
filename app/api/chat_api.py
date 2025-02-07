from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from typing import Annotated
from uuid import UUID

from ..models.user import User
from ..models.chat import Chat, ChatCreate, ChatPublic
from ..models.chat_member import ChatMember
from ..dependencies.common import get_session
from ..dependencies.security import GetCurrentUserFactory


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

