import requests
import json
import allure
from apps.cases.common.equitys_common.equity_apis import ProjectApi
from apps.cases.common.vxin_common.wx_yml import logindata_yml
from apps.cases.common.vxin_common.wxlogin_apis import WeiXinLogin
from apps.extensions.logger import log

logindata = logindata_yml()



class ProjectUserApis:

    def __init__(self):
        self.headers = logindata["headers"]

        #   拿微信公众号权益输入权益电子码接口数据
        self.url_v_project_user_check = logindata["v_project_user_check"]["url"]
        self.data_v_project_user_check = logindata["v_project_user_check"]["data"]
        #   拿确认激活权益接口数据
        self.url_v_equity_newactivate = logindata["v_equity_newActivate"]["url"]
        self.data_v_equity_newactivate = logindata["v_equity_newActivate"]["data"]

        self.equity = ProjectApi()
        self.wxlogin = WeiXinLogin()



    @allure.step("微信公众号激活电子码权益输入")
    def project_user_check(self):
        self.data_v_project_user_check["cdKey"] = self.equity.cdKey
        self.headers["Authorization"] = self.wxlogin.authorization
        try:
            resp = requests.post(url=self.url_v_project_user_check, data=json.dumps(self.data_v_project_user_check),
                                 headers=self.headers)
            res = resp.json()
            if res["errno"] == "0":
                print("激活电子码权益输入接口连接正常,PASS!")
                log.get_log("vxin_common", "INFO", "{},{},{}".format(self.url_v_project_user_check, self.data_v_project_user_check,
                            res))
                return res, self.url_v_project_user_check, self.data_v_project_user_check, self.headers
            else:
                print("激活电子码权益输入接口返回异常：{}".format(res))
                log.get_log("vxin_common", "INFO", "{},{},{}".format(self.url_v_project_user_check,
                            self.data_v_project_user_check, res))
                return False
        except Exception as e:
            print("激活电子码权益输入接口连接异常：{}".format(e))
            log.get_log("vxin_common", "INFO", "{},{},{}".format(self.url_v_project_user_check,
                        self.data_v_project_user_check, e))
            return False


    @allure.step("确认激活权益接口")
    def equity_newactivate(self):
        self.data_v_equity_newactivate["cdKey"] = self.equity.cdKey
        self.headers["Authorization"] = self.wxlogin.authorization
        try:
            resp = requests.post(url=self.url_v_equity_newactivate, data=json.dumps(self.data_v_equity_newactivate),
                                 headers=self.headers)
            res = resp.json()
            if res["errno"] == "0":
                print("确认激活权益接口接口连接正常,PASS!")
                log.get_log("vxin_common", "INFO", "{},{},{}".format(self.url_v_equity_newactivate,
                            self.data_v_equity_newactivate, res))
                return res, self.url_v_equity_newactivate, self.data_v_equity_newactivate, self.headers
            else:
                print("确认激活权益接口接口返回异常：{}".format(res))
                log.get_log("vxin_common", "INFO", "{},{},{}".format(self.url_v_equity_newactivate,
                            self.data_v_equity_newactivate, res))
                return False
        except Exception as e:
            print("确认激活权益接口接口连接异常：{}".format(e))
            log.get_log("vxin_common", "INFO", "{},{},{}".format(self.url_v_equity_newactivate,
                        self.data_v_equity_newactivate, e))
            return False





