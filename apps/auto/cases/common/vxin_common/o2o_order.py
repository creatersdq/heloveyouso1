import requests
import json
import allure
from apps.extensions.read_yml import file_yml
from apps.extensions.logger import log


class O2o_Order:

    def __init__(self):
        self.logindata = file_yml("vxin_common/wxdata.yml")
        self.o2oheaders = self.logindata["o2o_order"]["headers"]
        # o2o创建订单入参数据
        self.url_o2o_order = self.logindata["o2o_order"]["url"]
        self.data_o2o_order = self.logindata["o2o_order"]["data"]

    @allure.step("添加项目")
    def o2o_order(self, couponid):
        self.data_o2o_order["goodsList"][0]["coupons"][0]["couponId"] = couponid
        try:
            resp = requests.post(url=self.url_o2o_order, data=json.dumps(self.data_o2o_order),
                                 headers=self.o2oheaders)
            res = resp.json()
            if res["errno"] == "0":
                print("o2o创建订单接口连接通过,PASS!")
                log.get_log("vxin", "INFO", "{},{},{}".format(self.url_o2o_order, self.data_o2o_order, res))
                return res, self.url_o2o_order, self.data_o2o_order, self.o2oheaders
            else:
                print("o2o创建订单接口返回异常：{}".format(res))
                log.get_log("vxin", "DEBUG",
                            "{},{},{}".format(self.url_o2o_order, self.data_o2o_order, res))
                return False

        except Exception as e:
            print("o2o创建订单接口连接异常：{}".format(e))
            log.get_log("vxin", "ERROR", "{},{},{}".format(self.url_o2o_order, self.data_o2o_order, e))
            return False
