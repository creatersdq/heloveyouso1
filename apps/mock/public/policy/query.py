# -*- coding: utf-8 -*-
import json

from apps.curd.policy.crud_insure import get_task_no_config, get_policy_result
from apps.public.policy.policy_base import PolicyBase
from apps.public.sql_alchemy_encoder_del import AlchemyEncoder
from apps.curd.policy.curd_mongodb import get_mongodb_log
from apps.extensions.logger import log


class QueryBase(PolicyBase):
    """
    药品保-投保理赔数据查询
    """

    def __init__(
            self,
            dev: str
    ):
        super(QueryBase, self).__init__(dev)

    def query_task_no_data(
            self,
            task_no: str
    ) -> str:
        """
        获取投保任务关联表数据
        :param task_no:
        :return:
        """
        try:
            log.get_log(
                "policy_common",
                "INFO",
                "----------查询获取投保任务关联表数据----------"
            )
            # 查询数据库
            re = get_task_no_config(
                task_no=task_no,
                dev=self.dev
            )
            # sqlAlchemy对象转义json字符串
            re_del = json.dumps(
                re,
                cls=AlchemyEncoder,
                ensure_ascii=False
            )
            log.get_log(
                "policy_common",
                "INFO",
                "表数据查询结果：{}".format(re_del)
            )
            return re_del
        except Exception as e:
            log.get_log(
                "policy_common",
                "ERROR",
                "获取投保任务关联表数据失败:{}".format(e)
            )

    def query_insured_result(
            self,
            task_no: str
    ) -> str:
        """
        投保结果关联表数据查询
        :param task_no:
        :return:
        """
        try:
            log.get_log(
                "info",
                "INFO",
                "----------获取投保结果关联表数据----------"
            )
            # 查询数据库
            res = get_policy_result(
                task_no=task_no,
                dev=self.dev
            )
            # sqlAlchemy对象转义json字符串
            res_del = json.dumps(
                res,
                cls=AlchemyEncoder,
                ensure_ascii=False
            )
            log.get_log(
                "policy_common",
                "INFO",
                "表数据查询结果：{}".format(res_del)
            )
            return res_del
        except Exception as e:
            log.get_log(
                "policy_common",
                "ERROR",
                "获取投保结果关联表数据失败:{}".format(e)
            )

    def query_mongodb_data(
            self,
            collection: str,
            key: str,
            value: str
    ) -> str:
        """
        mongodb数据查询
        :param collection:
        :param key:
        :param value:
        :return:
        """
        try:
            log.get_log(
                "policy_common",
                "INFO",
                "----------查询mongodb日志----------"
            )
            # 查询mongo日志，
            res = get_mongodb_log(
                    collections=collection,
                    key=key,
                    value=value,
                    dev=self.dev
                )
            # 并转义为json字符串
            res = json.dumps(
                res,
                ensure_ascii=False
            )
            log.get_log(
                "policy_common",
                "INFO",
                "表数据查询结果：{}".format(res)
            )
            return res
        except Exception as e:
            log.get_log(
                "policy_common",
                "ERROR",
                "查询mongodb日志失败:{}".format(e)
            )


if __name__ == "__main__":
    p = QueryBase("test")
    a = p.query_task_no_data("TB220726005")
    # print(a)
    # b = p.query_insured_result("TB220726005")
    # print(b)
    # c = p.query_mongodb_data(collection='UniondrugSynGroupV3_0_policyDownload', key='originRequest',
    #                          value="PN165104111912177720939351862031")
    # print(c)
    # print(type(c))
    # print(json.loads(c))
    # print(type(json.loads(c)))
