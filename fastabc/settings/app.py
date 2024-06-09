from typing import Literal

from pydantic import Field

from fastabc import SkeletonModel


class AppModel(SkeletonModel):
    title: str = "Test"
    version: str = "1.0.0"
    env: Literal["dev", "prod", "test"] = "dev"
    debug: bool = False


class APIModel(AppModel):
    cors_origins: list[str] = Field(["*"])
    cors_headers: list[str] = Field(["*"])
    cors_methods: list[str] = Field(["*"])


class BotModel(AppModel):
    bot_token: str
