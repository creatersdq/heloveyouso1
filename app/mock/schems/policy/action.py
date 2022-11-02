from pydantic.main import BaseModel
from enum import Enum
from typing import Optional


class DEV(str, Enum):
    """
    环境
    """
    test = 'test'
    rc = 'rc'


class ACTIONTYPE(int, Enum):
    """
    操作类型
    """
    policyLogReset = 1  # 锁眼计划log清理
    invoicePush = 2  # 发票推送保司
    imagePush = 3  # 影像件推送保司


class PolicyAction(BaseModel):
    dev: DEV
    type: ACTIONTYPE
    registNo: Optional[str] = None  # 报案号
