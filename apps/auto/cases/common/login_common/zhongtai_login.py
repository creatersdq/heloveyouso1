import requests
import json
from apps.db_actions.login import get_token
from apps.extensions.logger import log
from apps.db_actions.common_case import update_config

# 登陆的手机号
mobile = "18317064763"


class zhongtai_login():


    @staticmethod
    def send_card():  # 获得验证码
        url = "http://uncenter.backend.turboradio.cn/sms/send"
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        data = {"mobile": mobile}

        try:
            resp = requests.post(url=url, data= json.dumps(data), headers=headers)
            res = resp.json()
            if res["errno"] == "0":
                print("获取验证码接口连接正常,PASS", res)
                data = get_token(mobile)
                card = data.captcha
                print(card)
                log.get_log("outapis", "INFO", "{},{},{},{}".format(url, data, res, card))
                return card
            else:
                print("获取验证码接口返回异常,ERROR", res)
                log.get_log("outapis", "INFO", "{},{},{}".format(url, data, res))
                return False
        except Exception as e:
            print("获取验证码接口连接异常,ERROR", e)
            log.get_log("outapis", "INFO", "{},{},{}".format(url, data, e))
            return False

    @staticmethod
    def mobile_login():  # 获得token
        card = zhongtai_login.send_card()
        print(card)
        url = "http://uncenter.backend.turboradio.cn/dd/mobilelogin"
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        data = {
                    "mobile": mobile,
                    "code": card
                }

        try:
            resp = requests.post(url=url, data= json.dumps(data), headers=headers)
            res = resp.json()
            if res["errno"] == "0":
                print("手机号登陆接口连接正常,PASS", res)
                token = res["data"]["token"]
                log.get_log("outapis", "INFO", "{},{},{},{}".format(url, data, res, token))
                return token
            else:
                print("手机号登陆接口返回异常,ERROR", res)
                log.get_log("outapis", "INFO", "{},{},{}".format(url, data, res))
                return False
        except Exception as e:
            print("手机号登陆接口连接异常,ERROR", e)
            log.get_log("outapis", "INFO", "{},{},{}".format(url, data, e))
            return False

    @staticmethod
    def dd_login():  # 获得 Authorization
        token = zhongtai_login.mobile_login()
        print(token)
        url = "http://uncenter.backend.turboradio.cn/dd/login"
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        data = {
            "token": token
        }
        try:
            resp = requests.post(url=url, data= json.dumps(data), headers=headers)
            res = resp.json()
            if res["errno"] == "0":
                print("登陆获得Authorization接口连接正常,PASS", res)
                Authorization = res["data"]["token"]
                print(Authorization)
                db_value = "Bearer "+Authorization
                print(db_value)
                update_config("营销中心", db_value)
                update_config("权益", db_value)
                log.get_log("outapis", "INFO", "{},{},{},{}".format(url, data, res, db_value))
                return db_value

            else:
                print("登陆获得Authorization接口返回异常,ERROR", res)
                log.get_log("outapis", "INFO", "{},{},{}".format(url, data, res))
                return False
        except Exception as e:
            print("登陆获得Authorization接口连接异常,ERROR", e)
            log.get_log("outapis", "INFO", "{},{},{}".format(url, data, e))
            return False
