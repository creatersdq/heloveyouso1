from apps.core.date_base import Base
from sqlalchemy import Column, String, Integer
from apps.core.timestamp_mixin import TimestampMixin


class TestPlan(Base, TimestampMixin):
    __tablename__ = 'test_plan'  # 表名
    __table_args__ = {'schema': 'cn_ud_quality_autotest'}  # 测试计划表
    id = Column(Integer, primary_key=True, unique=True)
    planNo = Column(String)  # 计划编号
    planName = Column(String)  # 计划名称
    type = Column(String)  # 1.接口自动化，2.性能测试
    projectId = Column(String)  # 项目id
    status = Column(String)  # 计划状态
    reportAddress = Column(String)  # 报告地址
