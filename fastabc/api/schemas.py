from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    msg: str
