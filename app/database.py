from sqlmodel import SQLModel, create_engine
from .config import settings


engine = create_engine(f'postgresql+psycopg://{settings.db.user}:{settings.db.password}'
f'@{settings.db.host}:{settings.db.port}/{settings.db.db_name}')


#  This will be later changed to migrations
def create_tables():
	SQLModel.metadata.create_all(engine)
