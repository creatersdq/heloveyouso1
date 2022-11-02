'''
获取数据库的相关操作
'''

from apps.core.test_date_base import session_maker
from apps.models.sms_table.smsdb import Message
from apps.models.equity_table.projectdb import (Projectdb, ProjectEquity, RedeemCode)
from apps.models.equity_table.equitydb import (GroupEquity, Equity)
import json


def to_dict(data):
    empty_list = []
    for i in data:
        d = {}
        for column in i.__table__.columns:
            d[column.name] = str(getattr(i, column.name))
        try:
            # d.pop('id')
            # d.pop('gmtCreated')
            # d.pop('gmtUpdated')
            empty_list.append(d)
        except Exception as e:
            raise e
    return empty_list


### 获取SMS库
# 获取sms_message表的数据
def get_message(mobile: str):
    with session_maker() as db:
        data = db.query(Message).filter(Message.mobile == mobile).order_by(Message.id.desc()).all()
        for each_row in data:
            return each_row.data
        # return data


# data = get_message("15157181383")
# print(data)
# print(to_dict(data))


# 获取Project库
# 获取project表的数据
def get_project(projectno: str):
    with session_maker() as db:
        data = db.query(Projectdb).filter(Projectdb.projectNo == projectno).all()
        for each_row in data:
            return each_row.data


# print(get_project("EPR202011067391"))

# 获取redeem_code表的数据
def get_redeem_code(cdKey: str):
    with session_maker() as db:
        data = db.query(RedeemCode).filter(RedeemCode.cdKey == cdKey).all()
        data = to_dict(data)
    return data


# 获取Equity库
# 获取group_equity表的数据
def get_group_equity(groupid: int):
    with session_maker() as db:
        # print(type(db))
        data = db.query(GroupEquity).filter(GroupEquity.groupId == groupid).all()
        for each_row in data:
            return each_row


# 获取equity表的数据
def get_equity(memberId: int):
    with session_maker() as db:
        data = db.query(Equity.equityNo, Equity.equityStatus).filter(Equity.memberId == memberId).order_by(
            Equity.activatedAt.desc()).all()
        for each_row in data:
            return each_row
