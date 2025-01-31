from sqlmodel import Session

# from .config import settings, DatabaseSettings
from .database import engine


async def get_session():
    with Session(engine) as session:
        yield session
