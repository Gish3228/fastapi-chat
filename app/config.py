from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class DatabaseSettings(BaseModel):
    host: str
    port: int
    user: str
    password: str
    db_name: str


class Settings(BaseSettings):
    db: DatabaseSettings
    model_config = SettingsConfigDict(env_file='.env', env_nested_delimiter='__')
