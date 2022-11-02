from sqlalchemy import Column, String, Integer
from app.core.data_base import Base
from app.core.timestamp_mixin import TimestampMixin


class LogNum(Base, TimestampMixin):
    __tablename__ = 'mock_db'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    proHost = Column(String(255))
    proAlias = Column(String(16))
    rcHost = Column(String(255))
    rcAlias = Column(String(16))
    proTableSchema = Column(String(255))
    rcTableSchema = Column(String(255))
    proTableName = Column(String(255))
    rcTableName = Column(String(255))
    logNum = Column(String(255))
    status = Column(String(1))
    num = Column(Integer)
    cycles = Column(Integer)


class DbNameAll(Base, TimestampMixin):
    __tablename__ = 'db_name_all'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    host = Column(String(255))
    asName = Column(String(255))
    port = Column(Integer)
    userName = Column(String(255))
    passWord = Column(String(255))
    envType = Column(String(255))
    status = Column(String(255))
