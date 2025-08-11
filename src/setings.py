from pathlib import Path

from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    base_url: str
    username: str
    password: str
    environment: str = "dev"

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env.test"
        env_file_encoding = "utf-8"


settings = Setting()
print(settings)

