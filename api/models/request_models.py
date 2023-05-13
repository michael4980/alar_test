'''Base models to validate requests and states'''
from pydantic import Field, BaseModel


class ValidModel(BaseModel):
    start: int = Field(ge=1)
    end: int = Field(ge=1)
