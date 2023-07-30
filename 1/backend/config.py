from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    VK_APP_ID: int
    VK_APP_SECRET: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
