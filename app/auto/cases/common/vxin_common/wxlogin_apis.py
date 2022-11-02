import requests
import json
import allure
from apps.cases.common.vxin_common.wx_yml import logindata_yml
from apps.db_actions.equity import get_message
from apps.extensions.logger import log

logindata = logindata_yml()


class WeiXinLogin:

    def __init__(self):
        self.headers = logindata["headers"]
        #   拿微信公众号登录获得验证码接口数据
        self.url_login_sendCaptcha = logindata["login_sendCaptcha"]["url"]
        self.data_login_sendCaptcha = logindata["login_sendCaptcha"]["data"]

        #   拿微信公众号登录接口数据
        self.url_login_login = logindata["login_login"]["url"]
        self.data_login_login = logindata["login_login"]["data"]

        self.authorization = ""

    # 微信公众号登录获得验证码接口
    @allure.step("微信公众号登录获得验证码")
    def login_sendCaptcha(self):
        try:
            resp = requests.post(url=self.url_login_sendCaptcha, data=json.dumps(self.data_login_sendCaptcha),
                                 headers=self.headers)
            res = resp.json()
            if res["errno"] == "0":
                print("微信公众号登录获得验证码接口连接通过,PASS!")
                log.get_log("vxin_common", "INFO", "{},{},{}".format(self.url_login_sendCaptcha, self.data_login_sendCaptcha, res))
                return res, self.url_login_sendCaptcha, self.data_login_sendCaptcha, self.headers
            else:
                print("微信公众号登录获得验证码接口返回异常：{}".format(res))
                log.get_log("vxin_common", "INFO", "{},{},{}".format(self.url_login_sendCaptcha, self.data_login_sendCaptcha, res))
                return False
        except Exception as e:
            print("微信公众号登录获得验证码接口连接异常：{}".format(e))
            log.get_log("vxin_common", "INFO", "{},{},{}".format(self.url_login_sendCaptcha, self.data_login_sendCaptcha, e))
            return False

    # 微信公众号登录接口
    @allure.step("微信公众号登录获取token")
    def login_login(self):
        # 微信公众号登录获取token
        mobile = self.data_login_login["mobile"]
        data = get_message(mobile)
        data1 = json.loads(data)
        code = data1["sms"]["code"]
        self.data_login_login["code"] = code
        try:
            resp = requests.post(url=self.url_login_login, data=json.dumps(self.data_login_login), headers=self.headers)
            res = resp.json()
            if res["errno"] == "0":
                token = res["data"]["token"]
                self.authorization = "Bearer " + token
                print("微信公众号登录接口连接通过,PASS!")
                log.get_log("vxin_common", "INFO", "{},{},{}".format(self.url_login_login, self.data_login_login, res))
                return res, self.url_login_login, self.data_login_login, self.headers
            else:
                print("微信公众号登录接口返回异常：{}".format(res))
                log.get_log("vxin_common", "INFO", "{},{},{}".format(self.url_login_login, self.data_login_login, res))
                self.authorization = ""
                return False
        except Exception as e:
            print("微信公众号登录接口连接异常：{}".format(e))
            log.get_log("vxin_common", "INFO", "{},{},{}".format(self.url_login_login, self.data_login_login, e))
            self.authorization = ""
            return False


