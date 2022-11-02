from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, Numeric, Date, DateTime
from apps.core.date_base import Base
from apps.core.timestamp_mixin import TimestampMixin


class Case(Base, TimestampMixin):
    __tablename__ = 'case_copy'  # 全映射
    __table_args__ = {'schema': 'cn_ud_quality_autotest'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    companyCode = Column(String)
    businessCode = Column(String)
    check_data = Column(Text)
    check_result = Column(Text)
    check_msg = Column(Text)
    url = Column(String)
    headers = Column(Text)
    data = Column(Text)
    return_msg = Column(Text)
    test_result = Column(Text)
    type = Column(String)
    test_status = Column(Integer)
    project_name = Column(String)
    project_id = Column(Integer)
    method = Column(String)
    test_reason = Column(Text)


class CaseRc(Base, TimestampMixin):
    __tablename__ = 'case'  # 全映射
    __table_args__ = {'schema': 'cn_ud_quality_autotest'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)           # case标题
    url = Column(String)            # 请求地址
    headers = Column(String)        # 请求头
    data = Column(Text)             # 请求结构体
    return_msg = Column(Text)       # 接口返回
    test_result = Column(Text)      # 测试结果
    type = Column(Integer)           # 类型
    test_status = Column(Integer)   # 未执行：0，成功：1，失败：2
    project_name = Column(String)   # 项目名
    project_id = Column(Integer)    # 项目id
    plan_name = Column(String)      # 测试计划
    plan_id = Column(Integer)       # 计划id
    method = Column(String)         # 请求方法

class Config(Base):
    __tablename__ = 'config'  # 全映射
    __table_args__ = {'schema': 'cn_ud_quality_autotest'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String)            # 关键字key
    value = Column(String)          # 关键字值
    belong = Column(String)         # 所属模块
    project_no = Column(String)     # 所属项目

