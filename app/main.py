from fastapi import FastAPI
from .api import user_api, auth_api, chat_api


app = FastAPI()
app.include_router(user_api.router, prefix='/users')
app.include_router(auth_api.router, prefix='/auth')
app.include_router(chat_api.router, prefix='/chats')

