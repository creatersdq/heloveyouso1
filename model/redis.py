
from typing import Optional
from pydantic.main import BaseModel


class RedisCurd(BaseModel):
    name: Optional[str] = None
    key: Optional[str] = None
    value: Optional[str] = None
