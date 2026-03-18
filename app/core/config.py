from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    ECHO_SQL: bool = False

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()