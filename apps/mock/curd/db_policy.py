from apps.core.data_base import session_maker
from apps.models.policy import Policy, PolicyInsurance


def call_back_policy_no(uuid, file_address, policy_no):
    """

    :param uuid:
    :param file_address:
    :param policy_no:
    :return: 保单号入库
    """
    with session_maker() as db:
        db.add(Policy(uuid=uuid, policy_no=policy_no, file_address=file_address))


def insurance_code_db(uuid, name, id_card, insurance_code):
    """

    :param uuid:
    :param name:
    :param id_card:
    :param insurance_code:
    :return: 投保码入库
    """
    with session_maker() as db:
        db.add(PolicyInsurance(uuid=uuid, name=name, id_card=id_card, insurance_code=insurance_code))


def get_claim_data():
    """
    查询保单
    :return:
    """
    with session_maker() as db:
        re = db.query(Policy.id, Policy.uuid, Policy.policy_no, Policy.file_address).all()
    return re


def get_insurance(uuid):
    """
    通过uuid查询理赔数据
    :param uuid:
    :return:
    """
    with session_maker() as db:
        re = db.query(PolicyInsurance.uuid,PolicyInsurance.insurance_code,PolicyInsurance.id_card,PolicyInsurance.name).filter(PolicyInsurance.uuid == uuid).all()
    return re


if __name__ == '__main__':
    a = []
    t = get_insurance("PN20211111104864")
    for g in t:
        insurance_code = t[1]
        pay_amount = 100
        partner_name = "一心堂药业集团股份有限公司"
        drug_info = "西黄胶囊"
        policy_no ="111"
        time = "2021/8/7 14:56:37"
        name = t[3]
        id_card = t[2]
        a.append([insurance_code,pay_amount,partner_name,drug_info,policy_no,time,name,id_card])
