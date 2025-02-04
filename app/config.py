from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class DatabaseSettings(BaseModel):
    host: str
    port: int
    user: str
    password: str
    db_name: str


class JWTSettings(BaseModel):
    secret_key: str
    algorithm: str
    token_expire_days: int


class Settings(BaseSettings):
    db: DatabaseSettings
    jwt: JWTSettings
    model_config = SettingsConfigDict(env_file='.env', env_nested_delimiter='__')
    


settings = Settings()
