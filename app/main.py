from fastapi import FastAPI
from .api import user_api


app = FastAPI()
app.include_router(user_api.router, prefix='/users')

