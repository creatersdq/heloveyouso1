from sqlalchemy import Column, String, Integer
from apps.core.data_base import Base
from apps.core.timestamp_mixin import TimestampMixin


class Policy(Base, TimestampMixin):
    __tablename__ = 'policy'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    uuid = Column(String(255))
    policy_no = Column(String(64))
    file_address = Column(String(255))


class PolicyInsurance(Base, TimestampMixin):
    __tablename__ = 'policy_insurance'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    uuid = Column(String(255))
    name = Column(String(255))
    id_card = Column(String(255))
    insurance_code = Column(String(64))


class HandleData(Base):
    __tablename__ = "qq"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    accountName = Column(String(255))
    bankAccount = Column(String(255))
    companyName = Column(String(255))
    damageAddress = Column(String(255))
    damageTime = Column(String(255))
    date = Column(String(255))
    insuredIdNo = Column(String(255))
    insuredIdNoAddress = Column(String(255))
    insuredIdNoEndDate = Column(String(255))
    insuredIdNoStartDate = Column(String(255))
    insuredName = Column(String(255))
    insuredTelephone = Column(String(255))
    isSeal = Column(String(255))
    openBankName = Column(String(255))
    policyNo = Column(String(255))
    idCard = Column(String(255))
    sign = Column(String(255))
    systemCode = Column(String(255))
    telephone = Column(String(255))
    status = Column(Integer)
    bsNo = Column(String(255))
    authorizationUrl = Column(String(255))
    powerUrl = Column(String(255))
    newStatus = Column(Integer)


class HandleDataBack(Base):
    __tablename__ = "qq_back"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    accountName = Column(String(255))
    bankAccount = Column(String(255))
    companyName = Column(String(255))
    damageAddress = Column(String(255))
    damageTime = Column(String(255))
    date = Column(String(255))
    insuredIdNo = Column(String(255))
    insuredIdNoAddress = Column(String(255))
    insuredIdNoEndDate = Column(String(255))
    insuredIdNoStartDate = Column(String(255))
    insuredName = Column(String(255))
    insuredTelephone = Column(String(255))
    isSeal = Column(String(255))
    openBankName = Column(String(255))
    policyNo = Column(String(255))
    idCard = Column(String(255))
    sign = Column(String(255))
    systemCode = Column(String(255))
    telephone = Column(String(255))
    status = Column(Integer)
    bsNo = Column(String(255))
    authorizationUrl = Column(String(255))
    powerUrl = Column(String(255))
    newStatus = Column(Integer)
