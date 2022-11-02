from sqlalchemy import Column, String, Integer, Text
from apps.core.date_base import Base
from apps.core.timestamp_mixin import TimestampMixin


class Case(Base, TimestampMixin):
    __tablename__ = 'case'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    name = Column(String)
    url = Column(String(255))
    headers = Column(Text())
    data = Column(Text())
    returnMsg = Column(Text())
    testResult = Column(Text())
    type = Column(String(12))
    testStatus = Column(Integer)
    projectName = Column(String(12))
    projectId = Column(Integer)
    planName = Column(String(12))
    planId = Column(Integer)
    method = Column(String(8))


class User(Base,TimestampMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    name = Column(String)
    account = Column(String)
    token = Column(String(255))


class AsyncTask(Base,TimestampMixin):
    __tablename__ = "asyncTask"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    asyncTaskName = Column(String(255))
    startWay = Column(String(16))
    status = Column(Integer)
    taskNo = Column(String(64))
    taskResult = Column(String(255))
