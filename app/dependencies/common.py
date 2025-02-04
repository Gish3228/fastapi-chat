from sqlmodel.ext.asyncio.session import AsyncSession

# from .config import settings, DatabaseSettings
from ..database import engine


async def get_session():
    async with AsyncSession(engine) as session:
        yield session
