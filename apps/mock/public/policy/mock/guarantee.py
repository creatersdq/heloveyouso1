import datetime
import json

import requests

from apps.public.do_read_yaml import read_case_data
from apps.public.policy.policy_base import PolicyBase
from apps.public.uuid_generate import random_no
from apps.extensions.logger import log


class Guarantee(PolicyBase):

    def __init__(self, dev):
        """
        :param dev: 环境
        """
        super(Guarantee, self).__init__(dev)
        self.data_guarantee = {}

    def order_data_mock(
            self,
            product_code: str,
            claim_pay_mode: int
    ) -> dict:
        """
        保障订单数据mock
        :param product_code:
        :param claim_pay_mode:
        :return:
        """
        try:
            # 获取接口相关信息
            request_url = self.gatway_domain + self.api_order_data_push
            request_data = self.data_order_data_push
            header = self.request_header
            # 生成随机订单号
            identification = "MOCK"
            random_num = random_no(20)
            order_no = identification + random_num
            self.data_guarantee["order_no"] = order_no
            # 请求入参处理
            request_data["orderNo"] = self.data_guarantee["order_no"]
            request_data["activateDate"] = self.today_time
            request_data["productInfoList"][0]["productCode"] = product_code
            request_data["productInfoList"][0]["claimPayMode"] = claim_pay_mode
            request_body = json.dumps(request_data)
            # 订单数据推送
            response = requests.post(
                request_url,
                data=request_body,
                headers=header
            ).text
            log.get_log(
                "policy_guarantee_data_mock",
                "INFO",
                "保障订单数据推送结束-请求地址:{},入参:{},返参:{}".format(
                    request_url,
                    request_body,
                    response
                )
            )
            return json.loads(response)
        except Exception as e:
            log.get_log(
                "policy_guarantee_data_mock",
                "ERROR",
                "保障订单数据推送失败：{}".format(e)
            )

    def claim_data_mock(
            self,
            product_code: str,
            claim_pay_mode: int,
            payment_type: int
    ) -> dict:
        """
        保障理赔数据mock
        :param product_code:
        :param claim_pay_mode:
        :param payment_type:
        :return:
        """
        try:
            # 获取接口相关信息
            request_url = self.gatway_domain + self.api_claim_data_push
            request_data = self.data_claim_data_push
            header = self.request_header
            # 随机生成发票code,发票号码
            random_invoice_num = random_no(6)
            # 请求入参处理
            request_data["reportorInfo"]["reportorTime"] = self.today_time
            request_data["claimInfo"]["securityProductCode"] = product_code
            request_data["claimInfo"]["claimPayMode"] = claim_pay_mode
            request_data["damageInfo"]["businessNo"] = self.data_guarantee["order_no"]
            request_data["damageInfo"]["equityNo"] = self.data_guarantee["order_no"]
            request_data["payInfo"]["paymenType"] = payment_type
            request_data["claimInfo"]["invoiceList"][0]["invoiceNumber"] = random_invoice_num
            request_data["claimInfo"]["invoiceList"][0]["invoiceNo"] = random_invoice_num
            request_data["claimInfo"]["invoiceList"][0]["invoiceDate"] = self.today_time
            request_data["damageInfo"]["damageDate"] = self.today
            request_body = json.dumps(request_data)
            # 保障理赔数据推送
            response = requests.post(
                request_url,
                data=request_body,
                headers=header
            ).text

            log.get_log(
                "policy_guarantee_data_mock",
                "INFO",
                "保障理赔数据推送结束-请求地址:{},入参:{},返参:{}".format(
                    request_url,
                    request_body,
                    response
                )
            )
            return json.loads(response)
        except Exception as e:
            log.get_log(
                "policy_guarantee_data_mock",
                "ERROR",
                "保障理赔数据推送失败：{}".format(e)
            )


if __name__ == "__main__":
    g = Guarantee("rc")
    a = g.order_data_mock(product_code="qdzc0707", claim_pay_mode=3)
    print(a)
    print(type(a))
    b = g.claim_data_mock(product_code="qdzc0707", claim_pay_mode=3, payment_type=2)
    print(b)
    print(type(b))
