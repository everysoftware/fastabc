from abc import ABC
from typing import Any, Annotated

from pydantic import BaseModel, Field

# https://fastapi.tiangolo.com/how-to/extending-openapi/
OpenAPIResponseType = dict[int | str, dict[str, Any]]


class StringErrorResponse(BaseModel):
    detail: Annotated[str, Field(min_length=1, max_length=1024)]


class ResponseGroup(ABC):
    @classmethod
    def create(cls) -> OpenAPIResponseType:
        """400 Bad Request, 403 Forbidden."""
        return {
            400: {
                "description": "Already exists",
                "model": StringErrorResponse,
            },
            403: {
                "description": "Access denied",
                "model": StringErrorResponse,
            },
        }

    @classmethod
    def create_many(cls) -> OpenAPIResponseType:
        """403 Forbidden."""
        return {
            403: {
                "description": "Access denied",
                "model": StringErrorResponse,
            }
        }

    @classmethod
    def get(cls) -> OpenAPIResponseType:
        """403 Forbidden, 404 Not Found"""
        return {
            404: {
                "description": "Not found",
                "model": StringErrorResponse,
            },
            403: {
                "description": "Access denied",
                "model": StringErrorResponse,
            },
        }

    @classmethod
    def get_many(cls) -> OpenAPIResponseType:
        """403 Forbidden."""
        return {
            403: {
                "description": "Access denied",
                "model": StringErrorResponse,
            }
        }

    @classmethod
    def update(cls) -> OpenAPIResponseType:
        """403 Forbidden, 404 Not Found."""
        return {
            404: {
                "description": "Not found",
                "model": StringErrorResponse,
            },
            403: {
                "description": "Access denied",
                "model": StringErrorResponse,
            },
        }

    @classmethod
    def delete(cls) -> OpenAPIResponseType:
        """403 Forbidden, 404 Not Found"""
        return {
            404: {
                "description": "Not found",
                "model": StringErrorResponse,
            },
            403: {
                "description": "Access denied",
                "model": StringErrorResponse,
            },
        }

    @classmethod
    def multi_response(cls, examples: dict[str | int, str]) -> dict[str, Any]:
        return {
            "content": {
                "application/json": {
                    "examples": {
                        code: {"summary": summary, "value": {"detail": code}}
                        for code, summary in examples.items()
                    }
                }
            },
            "model": StringErrorResponse,
        }
