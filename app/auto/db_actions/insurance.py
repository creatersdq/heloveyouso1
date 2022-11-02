'''
获取数据库的相关操作
'''
from apps.core.test_date_base import session_maker
from apps.models.insurance_table.systems import Systems, Config
from apps.models.insurance_table.policy import PolicyRecords, PolicyDetail, PolicyBranch
from apps.models.insurance_table.claim import *
from sqlalchemy import func


# 获取system_config表的数据
def get_config(companycode: str, rationtype: str):
    with session_maker() as db:
        # 获取保司状态
        status = db.query(Systems.status).filter(Systems.systemCode == companycode).first()[0]  # (1,)
        # 判断保司状态是否开启
        if status != 1:
            return False
        else:
            # 判断方案代码是否为空
            if rationtype != '':
                sysconfig = db.query(Config).filter(Config.systemCode == companycode, Config.rationType == rationtype,
                                                    Config.productType == 2).all()
                return sysconfig
            else:
                sysconfig = db.query(Config).filter(
                    Config.systemCode == companycode and Config.rationType is None).all()
                return sysconfig


# 根据机构代码、产品代码反查获取system_config表的数据
def get_config_turn(productcode: str, systemcode: str):
    with session_maker() as db:
        sysconfig = db.query(Config).filter(Config.systemCode == systemcode, Config.productCode == productcode).first()
        return sysconfig


# 获取policy_branch表的数据
def get_business_config(companycode: str, businessCode: str):
    with session_maker() as db:
        # 判断公司代码是否有值
        if businessCode != '':
            business_config = db.query(PolicyBranch).filter(PolicyBranch.systemCode == companycode,
                                                            PolicyBranch.businessDepartmentCode == businessCode
                                                            ).all()
            return business_config
        else:
            return False


# 根据billNo获取policy_records、policy_detail表的数据
def get_policy(billno: str):
    with session_maker() as db:
        policyrecords = db.query(PolicyRecords).filter(PolicyRecords.waterNo == billno).all()
        policyno = policyrecords[0].policyNo
        policydetail = db.query(PolicyDetail).filter(PolicyDetail.policyNo == policyno).all()
        return policyrecords, policydetail


# 根据系统标识和机构代码倒序获取policyNo数据(确定是否投保成功)，取一条
def get_policyno(syscode: str, buscode: str):
    with session_maker() as db:
        policyno = db.query(PolicyRecords.policyNo).filter(PolicyRecords.systemCode == syscode,
                                                           PolicyRecords.businessDepartmentCode == buscode).order_by(
            PolicyRecords.id.desc()).first()
        return policyno


# 根据保单号反查获取policy_records表的数据
def get_policy_turn(policyno: str):
    with session_maker() as db:
        policyrecords = db.query(PolicyRecords).filter(PolicyRecords.policyNo == policyno).first()
        return policyrecords


# 根据保单号获取policy_records表中的已报案金额sumClaim的值
def get_policy_sumclaim(policyno: str):
    with session_maker() as db:
        sum_policy_records = db.query(PolicyRecords.sumClaim).filter(PolicyRecords.policyNo == policyno).first()
        return sum_policy_records


# 根据批次报案号和保单号来获取claim_records表的数据、总金额和总条数
def get_claim_records(billno: str, policyno: str):
    with session_maker() as db:
        claim_records_data = db.query(ClaimRecords).filter(ClaimRecords.billNo == billno,
                                                           ClaimRecords.policyNo == policyno).all()
        sum_claim_records_data = db.query(func.sum(ClaimRecords.damageAmount), func.count(ClaimRecords.damageAmount)). \
            filter(ClaimRecords.billNo == billno, ClaimRecords.policyNo == policyno).first()

        return claim_records_data, sum_claim_records_data


# 根据subId来获取claim_records表的总金额、总条数
def get_sumclaim_subid(subid: str):
    with session_maker() as db:
        sum_claim_records = db.query(func.sum(ClaimRecords.damageAmount), func.count(ClaimRecords.damageAmount)). \
            filter(ClaimRecords.subId == subid).first()
        # 获取claim_sub_records表的数据
        claim_sub_data = db.query(ClaimSubRecords).filter(ClaimSubRecords.id == subid).first()
        return sum_claim_records, claim_sub_data


# 根据批次报案号和保单号来获取claim_batch_records表的数据
def get_claim_batch(billno: str, policyno: str):
    with session_maker() as db:
        claim_batch_data = db.query(ClaimBatch).filter(ClaimBatch.billNo == billno,
                                                       ClaimBatch.policyNo == policyno).one()
        # 根据保单号获取claim_batch_records表的总金额
        sum_batch_sumclaim = db.query(func.sum(ClaimBatch.sumClaim)).filter(ClaimBatch.policyNo == policyno).first()
        return claim_batch_data, sum_batch_sumclaim


# 根据系统代码和保单号倒序获取claim_batch_records表中的billNo的数据，取一条
def get_claimbillno(syscode: str, policyno: str):
    with session_maker() as db:
        claimbillno = db.query(ClaimBatch.billNo).filter(ClaimBatch.systemCode == syscode,
                                                         ClaimBatch.policyNo == policyno).order_by(
            ClaimBatch.id.desc()).first()
        return claimbillno


# 根据batchId和保单号来获取claim_sub_records表的数据
def get_claim_sub(policyno: str, batchid: str):
    with session_maker() as db:
        claim_sub_data = db.query(ClaimSubRecords).filter(ClaimSubRecords.policyNo == policyno,
                                                          ClaimSubRecords.batchId == batchid).all()
        return claim_sub_data


# 获取claim_per_records表的数据
def get_claim_per(policyno: str):
    with session_maker() as db:
        claim_per_data = db.query(ClaimPerRecords).filter(ClaimPerRecords.policyNo == policyno).all()
        return claim_per_data


# 获取claim_payinfo表的数据
def get_claim_payinfo(billno: str, policyno: str):
    batchid = get_claim_batch(billno, policyno)[0].id
    with session_maker() as db:
        claim_payinfo_data = db.query(ClaimPayinfo).filter(ClaimPayinfo.batchId == batchid).all()
        # 判断此批次是否有反洗钱信息
        if claim_payinfo_data == None:
            return []
        else:
            return claim_payinfo_data


# 获取claim_status_log表的数据
def get_claim_log(policyno: str, batchid: str):
    claim_sub_data = get_claim_sub(policyno, batchid)
    claimlog_list = []
    # print(len(claim_sub_data))
    for i in range(len(claim_sub_data)):
        subid = claim_sub_data[i].id
        with session_maker() as db:
            claimlog = db.query(ClaimLog).filter(ClaimLog.subId == subid).first()
            claimlog_list.append(claimlog)
    return claimlog_list  # 返回的是个对象列表 取值要类似claimlog_list[i].status

# a = get_policyno('GuoRenDrug','099100AF')[0]
# b = get_claimbillno('GuoRenDrug',a)
# # c = get_config_turn('YPB','GuoRenDrug')
# print(b)
# print(b[0][0])
# print(c.claimNumLimit)
# print(a[1][1])
# print(b[1][0])
# for i in range(len(a)) :('6200308001926000285',)
#
#     print(a[i].subId)
