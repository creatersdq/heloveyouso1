from pydantic.main import BaseModel


class MockDbScript(BaseModel):
    proHostId: int  # 获取数据的host_id
    rcHostId: int  # 插入数据的host_id
    proTableSchema: str  # 生产的库名
    proTableName: str  # 生产的表名
    rcTableSchema: str  # rc的库名
    rcTableName: str  # rc的表名
    cycles: int  # 循环的次数
    num: int  # 每次循环的数据量


class SelectLogNum(BaseModel):
    logNum: str  # 日志编号
    proHost: str  # 生产数据库的host
    proTableSchema: str  # 生产的库名
    rcTableName: str  # rc的表名


class SelectLog(BaseModel):
    logNum: str  # 日志编号


class SearchLog(BaseModel):
    pageNum: int = 1
    pageSize: int = 10
