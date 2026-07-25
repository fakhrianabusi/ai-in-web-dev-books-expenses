from pydantic_settings import BaseSettings


class GeneralSettings(BaseSettings):
    APP_TITLE: str = "Demo Title"
    VERSION: str = "0.0.0"

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


general_settings = GeneralSettings()
