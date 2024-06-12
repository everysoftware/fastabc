from typing import Literal

from pydantic import Field, BaseModel


class AppModel(BaseModel):
    title: str = "Test"
    version: str = "0.1.0"
    env: Literal["dev", "prod", "test"] = "dev"
    debug: bool = False


class APIModel(AppModel):
    cors_origins: list[str] = Field(["*"])
    cors_headers: list[str] = Field(["*"])
    cors_methods: list[str] = Field(["*"])


class BotModel(AppModel):
    bot_token: str
