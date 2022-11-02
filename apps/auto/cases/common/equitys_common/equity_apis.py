import requests
import json
import allure
from apps.cases.common.equitys_common.fileyml import file_yml, nam
from apps.extensions.logger import log
from apps.cases.common.login_common.zhongtai_login import zhongtai_login

# 调用登陆获得最新的token
token = zhongtai_login().dd_login()

file_yml = file_yml()
nam = nam()


class ProjectApi:

    def __init__(self):
        self.headers = file_yml["headers"]
        # 拿权益的token
        self.headers["Authorization"] = token
        #   拿新增项目接口测试数据
        self.url_project_add = file_yml["project_add"]["url"]
        self.data_project_add = file_yml["project_add"]["data"]
        #   拿新增项分组的接口数据
        self.url_group_add = file_yml["group_add"]["url"]
        self.data_group_add = file_yml["group_add"]["data"]
        #   拿更改项目的接口数据
        self.url_project_limit = file_yml["projectLimit_projectChangeLimit"]["url"]
        self.data_project_limit = file_yml["projectLimit_projectChangeLimit"]["data"]
        #   拿编辑分组的接口数据
        self.url_group_edit = file_yml["group_edit"]["url"]
        self.data_group_edit = file_yml["group_edit"]["data"]
        #   拿生成权益（新增一个兑换码）的接口数据
        self.url_redeem_add = file_yml["redeem_add"]["url"]
        self.data_redeem_add = file_yml["redeem_add"]["data"]

        self.project_id = ""
        self.merchant_id = ""
        self.group_id = ""
        self.cdKey = ""

    @allure.step("添加项目")
    def project_add(self):
        self.data_project_add["name"] = "脚本" + str(nam)
        try:
            resp = requests.post(url=self.url_project_add, data=json.dumps(self.data_project_add), headers=self.headers)
            res = resp.json()
            if res["errno"] == "0":
                self.project_id = res["data"]["projectId"]
                self.merchant_id = res["data"]["merchantId"]
                print("权益项目创建接口连接通过,PASS!")
                log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_project_add, self.data_project_add, res))
                return res, self.url_project_add, self.data_project_add, self.headers
            else:
                print("权益项目创建接口返回异常：{}".format(res))
                log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_project_add, self.data_project_add, res))
                return False
        except Exception as e:
            print("权益项目创建接口连接异常：{}".format(e))
            log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_project_add, self.data_project_add, e))
            return False

    @allure.step("新增项目分组")
    def group_add(self, casename):
        self.data_group_add["projectId"] = self.project_id
        self.data_group_add["merchantId"] = self.merchant_id
        self.data_group_add["name"] = "脚本新增" + str(nam) + " 项目 " + casename
        try:
            resp = requests.post(url=self.url_group_add, data=json.dumps(self.data_group_add), headers=self.headers)
            res = resp.json()
            if res["errno"] == "0":
                self.group_id = res["data"]["groupId"]
                print("新增项目分组接口连接通过,PASS!")
                log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_group_add, self.data_group_add, res))
                return res, self.url_group_add, self.data_group_add, self.headers
            else:
                print("接口返回异常：{}".format(res))
                log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_group_add, self.data_group_add, res))
                self.group_id = ""
                return False
        except Exception as e:
            print("接口连接异常：{}".format(e))
            log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_group_add, self.data_group_add, e))
            self.group_id = ""
            return False

    @allure.step("更改项目策略")
    def project_limit(self, params=None):
        params["projectId"] = self.project_id
        try:
            resp = requests.post(url=self.url_project_limit, data=json.dumps(params), headers=self.headers)
            res = resp.json()
            if res["errno"] == "0":
                print("更改项目策略接口连接通过,PASS!")
                log.get_log("equitys_common", "INFO", "{},{}{}".format(self.url_project_limit, params,res))
                return res, self.url_project_limit, self.data_project_limit, self.headers
            else:
                print("接口返回异常：{}".format(res))
                log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_project_limit, params, res))
                return False
        except Exception as e:
            print("接口连接异常：{}".format(e))
            log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_project_limit, params, e))
            return False

    @allure.step("编辑项目分组")
    def group_edit(self):
        # 用新增项目分组接口返回的参数groupId,merchantId,projectId入参
        self.data_group_edit["data"]["groupId"] = self.group_id
        self.data_group_edit["data"]["merchantId"] = self.merchant_id
        self.data_group_edit["data"]["projectId"] = self.project_id
        try:
            resp = requests.post(url=self.url_group_edit, data=json.dumps(self.data_group_edit), headers=self.headers)
            res = resp.json()
            if res["errno"] == "0":
                print("编辑项目分组接口连接通过,PASS!")
                log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_group_edit, self.data_group_edit, res))
                return res, self.url_group_edit, self.data_group_edit, self.headers
            else:
                print("接口返回异常：{}".format(res))
                log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_group_edit, self.data_group_edit, res))
                return False
        except Exception as e:
            print("接口连接异常：{}".format(e))
            log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_group_edit, self.data_group_edit, e))
            return False

    @allure.step("单个生成权益【新增一个兑换码】")
    def redeem_add(self):
        # 用新增项目分组接口返回的参数入参
        self.data_redeem_add["projectId"] = self.project_id
        self.data_redeem_add["merchantId"] = self.merchant_id
        self.data_redeem_add["groupId"] = self.group_id
        try:
            resp = requests.post(url=self.url_redeem_add, data=json.dumps(self.data_redeem_add), headers=self.headers)
            res = resp.json()
            if res["errno"] == "0":
                self.cdKey = res["data"]["verify"]["cdKey"]  # 权益电子码激活权益需要
                print("单个生成权益接口连接通过,PASS!")
                log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_redeem_add, self.data_redeem_add, res))
                return res, self.url_redeem_add, self.data_redeem_add, self.headers
            else:
                print("接口返回异常：{}".format(res))
                log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_redeem_add, self.data_redeem_add, res))
                self.cdKey = ""
                return False
        except Exception as e:
            print("接口连接异常：{}".format(e))
            log.get_log("equitys_common", "INFO", "{},{},{}".format(self.url_redeem_add, self.data_redeem_add, e))
            self.cdKey = ""
            return False
