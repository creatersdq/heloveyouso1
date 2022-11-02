import datetime

from app.extensions.logger import log
from app.curd.db_common import session_set
from app.models.policy.insure import PolicyRecords, PolicyObject, ClaimRecords, ClaimBatchRecords, PolicyPlanLog, \
    PolicyBatchRecords, PolicyFileRecords, PolicyRule, BsSaleRecords, BsProducts, BranchConfig, SystemConfig, BsBranch, \
    PolicyDetail, BsProductsRation, QdPolicyPlanExtra

db_name = "yl_"


def get_policy_object(
        policy_no: str,
        dev: str
) -> any:
    """
    :param dev:
    :param policy_no: 保单号
    :return:
    """
    with session_set(dev=db_name + dev) as db:
        water_no = db.query(PolicyRecords.waterNo).filter(PolicyRecords.policyNo == policy_no).first()
        res = db.query(PolicyObject).filter(PolicyObject.waterNo == water_no[0]).all()
        return res


def get_claim_records(
        batch_id: str,
        dev: str
) -> any:
    """

    :param batch_id:
    :param dev:
    :return:
    """
    with session_set(dev=db_name + dev) as db:
        try:
            res = db.query(ClaimRecords).filter(ClaimRecords.batchId == batch_id).all()
        except Exception as e:
            log.get_log(
                "policy_db_action",
                "ERROR",
                "数据库查询异常:{}".format(e)
            )

    return res


def get_batch_no(
        bill_no: str,
        dev: str
):
    """

    :param bill_no:
    :param dev:
    :return:
    """
    with session_set(dev=db_name + dev) as db:
        try:
            res = db.query(ClaimBatchRecords).filter(ClaimBatchRecords.billNo == bill_no).first()
        except Exception as e:
            log.get_log(
                "policy_db_action",
                "ERROR",
                "数据库查询异常:{}".format(e)
            )
    return res.id


def policy_log_reset(
        dev: str
) -> any:
    """
    锁眼计划log清理，便于脚本重复执行
    :param dev: 环境：test，rc
    :return:
    """
    data = {"date": "0"}
    with session_set(dev=db_name + dev) as db:
        try:
            res = db.query(PolicyPlanLog).filter(
                PolicyPlanLog.date >= datetime.datetime.now().strftime('%Y-%m-%d')).update(
                data)
        except Exception as e:
            log.get_log(
                "policy_db_action",
                "INFO",
                "数据库查询异常:{}".format(e)
            )
    return res


def get_task_no_config(
        dev: str,
        task_no: str
) -> any:
    """
    投保任务关联表数据查询
    :param task_no: 投保单号
    :param dev:
    :return:
    """
    res = {}
    with session_set(dev=db_name + dev) as db:
        try:
            data_policy_batch = db.query(PolicyBatchRecords).filter(
                PolicyBatchRecords.taskNo == task_no).first()
            res["policy_batch_records"] = data_policy_batch
            res["policy_object_records"] = db.query(PolicyObject).filter(
                PolicyObject.waterNo == res["policy_batch_records"].waterNo).all()
            res["bs_sales"] = db.query(BsSaleRecords).filter(BsSaleRecords.id == data_policy_batch.bsSaleId).first()
            res["bs_products"] = db.query(BsProducts).filter(BsProducts.id == data_policy_batch.bsProductId).first()
            res["policy_rule"] = db.query(PolicyRule).filter(PolicyRule.id == res["bs_sales"].policyRuleId).first()
            res["system_config"] = db.query(SystemConfig).filter(
                SystemConfig.id == res["bs_sales"].systemConfigId).first()
            res["bs_branch"] = db.query(BsBranch).filter(BsBranch.id == data_policy_batch.bsBranchId).first()
            res["branch_config_1"] = db.query(BranchConfig).filter(
                BranchConfig.bsProductId == res["bs_products"].id,
                BranchConfig.bsBranchParentId == res["bs_branch"].parentId).first()
            res["bs_product_ration"] = db.query(BsProductsRation).filter(
                BsProductsRation.bsProductId == res["bs_products"].id).first()
            policy_plan_log = db.query(PolicyPlanLog).first()
            res["qd_policy_plan_extra"] = db.query(QdPolicyPlanExtra).filter(
                QdPolicyPlanExtra.qdPolicyPlanRuleId == policy_plan_log.qdPolicyPlanRuleId).first()
        except Exception as e:
            log.get_log(
                "policy_db_action",
                "INFO",
                "数据库查询异常:{}".format(e)
            )
    return res


def get_policy_result(
        dev: str,
        task_no: str
) -> any:
    """
    投保结果关联表数据查询
    :param dev:
    :param task_no:
    :return:
    """
    res = {}
    with session_set(dev=db_name + dev) as db:
        try:
            data_policy_batch = db.query(PolicyBatchRecords).filter(
                PolicyBatchRecords.taskNo == task_no).first()
            res["policy_batch_records"] = data_policy_batch
            res["policy_records"] = db.query(PolicyRecords).filter(PolicyRecords.batchId == data_policy_batch.id).first()
            res["policy_file_records"] = db.query(PolicyFileRecords).filter(
                PolicyFileRecords.batchId == data_policy_batch.id).first()
            res["policy_detail"] = db.query(PolicyDetail).filter(
                PolicyDetail.policyId == res["policy_records"].id).first()
        except Exception as e:
            log.get_log(
                "policy_db_action",
                "INFO",
                "数据库查询异常:{}".format(e)
            )
        return res


def insert_db_data(
        dev: str,
        insert_data: dict
) -> any:
    data_in = insert_data
    with session_set(dev=db_name + dev) as db:
        res = db.add_all(data_in)


def insert_claim_pay_info(
        dev: str,
        insert_data
) -> any:
    data_in = insert_data
    with session_set(dev=db_name + dev) as db:
        res = db.add_all(data_in)


if __name__ == '__main__':
    c = get_policy_object(policy_no='6390080101820220000230', dev="test")
    print(type(c))
    # e = get_batch_no('TN202207218059776168965978064319', 'test')
    # print(e)
    # d = get_claim_records(e, 'test')
    # print(d[1].damageNo)
    # policy_log_reset('test')
    # h = get_task_no_config(dev='test', task_no='TB220726005')
    # print(h)
    # i = get_task_no_config(dev='test', task_no='TB220726005')
    # print(i)
    # insert_list = []
    # data = ClaimSubRecords(batchId=288191, waterNo='UG220726491011019854555153499785', registNo='1',
    #                        policyNo="2049101002022300004", systemCode="PropertyInsuranceDrug", partnerCode="20",
    #                        totalNum=1, totalAmount=7.92, sumClaim=0, sumClaimed=0, sumClaimPaid=0,
    #                        claimTime='2022-08-03 15:20:40', status='07')
    # insert_list.append(data)
    # insert_claim_sub(dev='test', insert_data=insert_list)
    # print(len(d))
