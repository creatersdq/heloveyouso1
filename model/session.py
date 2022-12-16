
from typing import Optional
from pydantic.main import BaseModel


class Param(BaseModel):
    url: Optional[str] = None
    body: Optional[str] = None
