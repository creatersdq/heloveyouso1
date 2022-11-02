import json

import requests

from apps.cases.common.insurance_common.do_read_yaml import read_case_data
from apps.extensions.logger import log


class Claim_Base(object):

    def __init__(self, dev: str):
        self.dev = dev  # 环境
        self.data_base = read_case_data('common.yaml')  # 读取配置文件
        # 域名
        self.domain_test = self.data_base["COMMON_DOMAIN_NAME_RC"]["TEST_MOCK"]
        # API
        self.api_policy_data_mock = self.data_base["API"]["POLICY_DATA_MOCK"]
        self.api_policy_common_action = self.data_base["API"]["POLICY_COMMON_ACTION"]
        self.api_policy_common_query = self.data_base["API"]["POLICY_COMMON_QUERY"]
        # 入参
        self.data_policy_data_mock = self.data_base["DATA"]["POLICY_DATA_MOCK"]
        self.data_policy_common_action = self.data_base["DATA"]["POLICY_COMMON_ACTION"]
        self.data_policy_common_query = self.data_base["DATA"]["POLICY_COMMON_QUERY"]

        self.headers = self.data_base["COMMON_HEADERS"]["HEADERS_JSON"]  # headers

    def claim_data_push(self, policy_no: str) -> dict:
        """
        理赔数据推送-理赔批次、发票、订单影像件
        @return:
        """
        try:
            log.get_log("insurance_interconnection", "INFO",
                        "----------理赔数据推送开始-policyNO：{}----------".format(policy_no))
            request_url = self.domain_test + self.api_policy_data_mock
            request_data = self.data_policy_data_mock
            request_headers = self.headers
            request_data["dev"] = self.dev
            request_data["switchConfig"]["orderDataMock"] = 0
            request_data["switchConfig"]["claimDataMock"] = 1
            request_data["switchConfig"]["invoiceDataMock"] = 1
            request_data["switchConfig"]["orderRecordsMock"] = 1
            request_data["switchConfig"]["orderAttachmentDataMock"] = 1
            request_data["claimDetail"]["policyNo"] = policy_no
            request_data = json.dumps(request_data)
            res = requests.post(request_url, data=request_data, headers=request_headers).json()
            log.get_log("insurance_interconnection", "INFO",
                        "----------理赔数据推送结果-result：{}----------".format(res))
            return res
        except Exception as e:
            log.get_log("insurance_interconnection", "INFO", "理赔数据推送失败:{}".format(e))


if __name__ == '__main__':
    c = Claim_Base('test')
    n = c.claim_data_push("6390080101820220000243")
    print(n)
    print(n["errno"])
    print(type(n))

