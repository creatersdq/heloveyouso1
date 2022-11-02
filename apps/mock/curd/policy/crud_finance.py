from apps.models.policy.finance import Pool_Claim
from apps.curd.db_common import session_set
from apps.extensions.logger import log


def order_reset(
        pool_id_list: list,
        update_data,
        dev
) -> any:
    """
    重置待理赔池-订单投保状态
    :param update_data:
    :param dev: 环境，test：测试 rc：rc
    :param pool_id_list: pool_claim.id 列表
    :return:
    """
    dev = "cw_" + dev
    with session_set(dev) as db:
        try:
            for pool_id in pool_id_list:
                db.query(Pool_Claim).filter(Pool_Claim.id == pool_id).update(update_data)
                return res
        except Exception as e:
            log.get_log(
                "policy_db_action",
                "ERROR",
                "重置药品保待理赔池失败：{}".format(e)
            )


def get_pool_claim(
        pool_id: list,
        dev: str
) -> list:
    """
    查询待理赔池-订单数据
    :param dev: 环境，test：测试 rc：rc
    :param pool_id: pool_claim.id
    :return:
    """
    dev = "cw_" + dev
    with session_set(dev) as db:
        try:
            res = db.query(Pool_Claim).filter(Pool_Claim.id.in_(pool_id)).all()
            return res
        except Exception as e:
            log.get_log(
                "policy_db_action",
                "ERROR",
                "查询财务待理赔池-订单数据失败：{}".format(e)
            )


if __name__ == '__main__':
    id_list = [124855, -1]
    id = [127096,
          127083,
          127061,
          127028,
          126986,
          126889,
          126852]
    order_reset(id_list, {"statement_no": ""}, "test")
    res = get_pool_claim
    print(res(id, "test"))
