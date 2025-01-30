from .config import Settings, DatabaseSettings


settings = Settings()


def get_db_settings() -> DatabaseSettings:
    return settings.db
