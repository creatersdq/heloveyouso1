from pydantic.main import BaseModel
from enum import Enum
from typing import Optional


class DEV(str, Enum):
    """
    环境
    """
    test = 'test'
    rc = 'rc'


class QUERYTYPE(int, Enum):
    """
    查询类型
    """
    insureBatchQuery = 1  # 投保任务数据查询
    insureResultQuery = 2  # 投保结果数据查询
    mongodbQuery = 3  # mongodb日志查询


class PolicyQuery(BaseModel):
    dev: DEV
    type: QUERYTYPE
    taskNo: Optional[str] = None  # 投保单号
    mongoDBCollection: Optional[str] = None  # mongoDB集合名称
    mongoDBKey: Optional[str] = None  # mongoDB 查询key
    mongoDBValue: Optional[str] = None  # mongoDB 查询value
