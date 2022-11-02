from apps.core.date_base import Base
from sqlalchemy import Column, String, Integer
from apps.core.timestamp_mixin import TimestampMixin


class TestProject(Base, TimestampMixin):
    __tablename__ = 'project'  # 表名
    __table_args__ = {'schema': 'cn_ud_quality_autotest'}  # 测试项目表
    id = Column(Integer, primary_key=True, unique=True)
    projectName = Column(String)  # 项目名称
    projectNo = Column(String)  # 项目编号
    commont = Column(String)  # 项目标注
    belonger = Column(String)  # 项目归属人
    status = Column(String)  # 默认0，正使用
    reportAddress = Column(String)  # 报告地址
    type =  Column(Integer) # '项目类型：1.自动化 2.功能 3.其他'
