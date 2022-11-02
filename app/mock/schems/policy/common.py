from typing import Optional

from pydantic import BaseModel


class Server(BaseModel):
    entryName: Optional[str]
    dev: Optional[str]
    commList: Optional[list]


class ServerLog(BaseModel):
    serverDirName: Optional[str]
    daysRetrospective: Optional[int]
    readComm: Optional[str]


class connDetail(BaseModel):
    serverDetail: Optional[Server]
    serverLogDetail: Optional[ServerLog] = None
