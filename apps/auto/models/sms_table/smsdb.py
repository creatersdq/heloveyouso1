from sqlalchemy import Column, String, Integer, Text
from apps.core.test_date_base import Base


class Message(Base):
    __tablename__ = 'message'  # 全映射表
    __table_args__ = {'schema': 'cn_uniondrug_module_sms'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String)
    mobile = Column(String)
    filterTag = Column(String)
    data = Column(Text)


class OutMessage(Base):
    """药联中台短信表"""
    __tablename__ = 'message'  # 全映射表
    __table_args__ = {'schema': 'outreach_msg'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, autoincrement=True)
    mobile = Column(String)
    content = Column(Text)


class CaptCha(Base):
    """药联中台登陆短信验证码表"""
    __tablename__ = 'captcha'  # 全映射表
    __table_args__ = {'schema': 'cn_uniondrug_module_data'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, autoincrement=True)
    mobile = Column(String)
    captcha = Column(String)



