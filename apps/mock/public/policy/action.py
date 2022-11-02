from apps.curd.policy.crud_insure import policy_log_reset
from apps.extensions.logger import log
from apps.public.do_read_yaml import read_case_data

import requests

from apps.public.policy.policy_base import PolicyBase


class ActionBase(PolicyBase):
    """
    药品保-常用操作模拟
    """

    def __init__(self, dev: str):
        """
        :param dev: 环境
        """
        super(ActionBase, self).__init__(dev)

    def policy_log_action(self) -> any:
        """
        锁眼计划log清理，便于脚本重复执行
        :return:
        """
        try:
            log.get_log(
                "policy_common",
                "ERROR",
                "----------锁眼计划日志清理开始-----------"
            )
            policy_log_reset(self.dev)
            log.get_log(
                "policy_common",
                "ERROR",
                "----------锁眼计划日志清理结束----------"
            )
        except Exception as e:
            log.get_log(
                "policy_common",
                "ERROR",
                "锁眼计划日志清理异常：{}".format(e)
            )

    def invoice_push(
            self,
            regist_no: str
    ) -> any:
        """
        发票推送保司
        :param regist_no: 报案号
        :return:
        """
        try:
            log.get_log(
                "info",
                "INFO",
                "----------发票推送保司开始----------"
            )
            url = self.module_domain + self.api_invoice_push
            body = {"registNo": regist_no}
            response = requests.post(
                url=url,
                data=body,
                headers=self.request_header
            ).text

            log.get_log(
                "policy_common",
                "INFO",
                "url:{},入参:{}，返参:{}\n----------发票推送保司结束----------".format(
                    url,
                    body,
                    response)
            )

        except Exception as e:
            log.get_log(
                "policy_common",
                "ERROR",
                "发票推送保司异常:{}".format(e)
            )

    def image_push(
            self,
            regist_no: str
    ) -> any:
        """
        影像件推送保司
        :param regist_no: 报案号
        :return:
        """
        try:
            log.get_log(
                "policy_common",
                "INFO",
                "----------影像件推送保司开始----------"
            )
            url = self.module_domain + self.api_image_push
            body = {"registNo": regist_no}
            response = requests.post(
                url=url,
                data=body,
                headers=self.request_header
            ).text
            log.get_log(
                "policy_common",
                "INFO",
                "url:{},入参:{}，返参:{}\n----------影像件推送保司结束----------".format(
                    url,
                    body,
                    response
                )
            )
        except Exception as e:
            log.get_log(
                "policy_common",
                "ERROR",
                "发票推送保司异常:{}".format(e)
            )


if __name__ == "__main__":
    p = ActionBase(dev="test")
    p.policy_log_action()
    p.image_push("20220726001")
    p.invoice_push("20220726001")
