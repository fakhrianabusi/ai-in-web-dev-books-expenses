from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    DATABASE_URL: str = ""
    ECHO: bool = True

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


database_settings = DatabaseSettings()
