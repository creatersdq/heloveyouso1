'''
获取数据库的相关操作
'''

from apps.core.test_date_base import session_maker
from apps.models.promotecenter_table.pc_user_card import PcUserCard
from apps.models.sms_table.smsdb import OutMessage
from apps.models.case_copy import Config


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



# 获取pc_user_card表数据
def get_pc_user_card(member_id: int):
    with session_maker() as db:
        data = db.query(PcUserCard).filter(PcUserCard.member_id == member_id).all()
        data = to_dict(data)
    return data

# data = get_pc_user_card(15965639)
# print(data)


def delete_pc_user_card(member_id: int):
    with session_maker() as db:
        db.query(PcUserCard).filter(PcUserCard.member_id == member_id).delete()

# delete_pc_user_card(15965886)

def get_uniondrug_login(mobile: int):
    with session_maker() as db:
        data = db.query(OutMessage).filter(OutMessage.mobile == mobile).order_by(OutMessage.id.desc()).all()
        data_new = to_dict(data)
    return data_new
# a = get_uniondrug_login(15157181383)
# print(a)


def get_config(id: int):
    with session_maker() as db:
        data = db.query(Config.value).filter(Config.id == id).all()
        return data[0][0]


# # 修改config表token
# def update_config(belong: str, value: str):
#     with session_maker() as db:
#         db.query(Config).filter(Config.belong==belong).update({"value": value})
