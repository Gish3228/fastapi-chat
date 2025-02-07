from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from .config import settings


engine = create_async_engine(f'postgresql+psycopg_async://{settings.db.user}:{settings.db.password}'
f'@{settings.db.host}:{settings.db.port}/{settings.db.db_name}')


#  This will be later changed to migrations
async def create_tables():
	async with engine.begin() as conn:
		await conn.run_sync(SQLModel.metadata.drop_all)
		await conn.run_sync(SQLModel.metadata.create_all)

