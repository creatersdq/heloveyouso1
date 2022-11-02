from apps.core.data_base import session_maker
from apps.models.policy import HandleData, HandleDataBack


def get_authorization_date() -> any:
    """
    获取生成理赔申请书原数据
    :return:
    """
    with session_maker() as db:
        res = db.query(HandleData.accountName, HandleData.bankAccount, HandleData.companyName,
                       HandleData.damageAddress,
                       HandleData.damageTime, HandleData.date, HandleData.insuredIdNo,
                       HandleData.insuredIdNoAddress,
                       HandleData.insuredIdNoEndDate, HandleData.insuredIdNoStartDate,
                       HandleData.insuredName,
                       HandleData.insuredTelephone, HandleData.openBankName, HandleData.policyNo,
                       HandleData.sign,
                       HandleData.id, HandleData.status, HandleData.bsNo).filter(
            HandleData.newStatus == 0).all()
    return res


# 理赔申请书
def update_status(back_qq_id: int, authorization_url: str):
    with session_maker() as db:
        db.query(HandleData).filter(HandleData.id == back_qq_id).update(
            {"newStatus": 1, "authorizationUrl": authorization_url})


# 获取生成理赔授权书原数据
def get_power_date() -> any:
    with session_maker() as db:
        res = db.query(HandleData.insuredIdNo, HandleData.insuredName, HandleData.policyNo, HandleData.sign,
                       HandleData.id, HandleData.status).filter(
            HandleData.status != 2, HandleData.sign != "0").all()
    return res


# 理赔授权书
def update_sq_status(qq_id: int, power_url: str):
    with session_maker() as db:
        db.query(HandleData).filter(HandleData.id == qq_id).update({"status": 2, "powerUrl": power_url})


if __name__ == '__main__':
    print(len(get_power_date()))
