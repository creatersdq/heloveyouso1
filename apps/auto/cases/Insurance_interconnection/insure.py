import json
import requests

from parse import search
from apps.extensions.logger import log
from apps.cases.common.insurance_common.datetime_cal import DateCal
from apps.cases.common.insurance_common.xml_data_del import xml_analysis
from apps.cases.common.insurance_common.server_base import ServerBase
from apps.cases.common.insurance_common.cases_config import common_config, server_config


class InsureBase(object):

    def __init__(self, dev: str):
        self.dev = dev  # 环境
        self.entry_name = "module.outreach.equity.claim"  # 脚本项目名称
        # 获取配置
        self.data_base = common_config
        self.server_config = server_config
        # 域名
        self.domain_test_mock = self.data_base["COMMON_DOMAIN_NAME_RC"]["TEST_MOCK"]
        # API
        self.api_mock = self.data_base["API"]["POLICY_DATA_MOCK"]
        self.api_action = self.data_base["API"]["POLICY_COMMON_ACTION"]
        self.api_query = self.data_base["API"]["POLICY_COMMON_QUERY"]
        # 预设入参
        self.request_data_mock = self.data_base["DATA"]["POLICY_DATA_MOCK"]
        self.request_data_action = self.data_base["DATA"]["POLICY_COMMON_ACTION"]
        self.request_data_query = self.data_base["DATA"]["POLICY_COMMON_QUERY"]

        self.headers = self.data_base["COMMON_HEADERS"]["HEADERS_JSON"]  # headers
        self.res_pre_insured = None  # 预投保关联表数据
        self.res_actual_insured = None  # 投保结果关联表数据
        self.expect_insured = None  # 预期保费，保额，保期
        self.log_insured = None  # 请求保司投保日志
        self.log_pool_amount = None  # 请求南京资金池金额日志
        self.log_policy_task = None  # 请求南京预投保日志

        # 初始化服务器连接
        self.server_client = ServerBase(dev=self.dev, entry_name=self.entry_name)

    def get_pre_insured(self, task_no: str) -> str:
        """
        获取预投保-关联表数据
        :param:
        :return:
        """
        try:
            request_url = self.domain_test_mock + self.api_query
            request_data = self.request_data_query
            # 组装请求入参
            request_data["type"] = 1
            request_data["dev"] = self.dev
            request_data["taskNo"] = task_no
            # 请求接口
            response_data = requests.post(request_url, headers=self.headers, data=json.dumps(request_data)).json()
            log.get_log("insurance", "INFO",
                        "锁眼计划-获取预投保关联表数据-请求地址:{},入参:{},返参:{}".format(request_url, request_data, response_data))
            # 返参数据提取
            self.res_pre_insured = response_data["data"]
            return response_data["errno"]
        except Exception as e:
            log.get_log("insurance", "ERROR", "锁眼计划-获取预投保关联表数据失败:{}".format(e))

    def get_actual_insured(self, task_no: str) -> str:
        """
        获取实际投保结果-关联表数据
        @param task_no: 投保单号
        @return:
        """
        try:
            request_url = self.domain_test_mock + self.api_query
            request_data = self.request_data_query
            # 组装请求参数
            request_data["type"] = 2
            request_data["dev"] = self.dev
            request_data["taskNo"] = task_no
            # 请求接口
            response_data = requests.post(request_url, headers=self.headers, data=json.dumps(request_data)).json()
            # 返参数据提取
            self.res_actual_insured = response_data["data"]
            log.get_log("insurance", "INFO",
                        "获取投保结果-请求地址:{},入参:{},返参:{}".format(request_url, request_data, response_data))
            return response_data["errno"]
        except Exception as e:
            log.get_log("insurance", "ERROR", "获取投保结果失败:{}".format(e))

    def cal_except_res(self) -> any:
        """
        预期保费，保额，保期计算
        """
        try:
            # 获取关联表数据
            policy_object_records = self.res_pre_insured["policy_object_records"]
            bs_products_records = self.res_pre_insured["bs_products"]
            bs_product_ration = self.res_pre_insured["bs_product_ration"]
            # 提取关键字段
            policy_period = bs_products_records["policyPeriod"]  # 保险期间
            policy_period_type = bs_products_records["policyPeriodType"]  # 保险期间类型，1：年，2：月 3：天
            effect_num = bs_products_records["effectNum"]  # 生效间隔日
            ration_type = bs_product_ration["rationType"]  # 方案模型 1：固定 2：不固定
            premium_rate = bs_product_ration["premiumRate"]  # 标准费率
            premium = bs_product_ration["premium"]  # 标准保费

            # 预期保费、保额计算
            sum_premium = 0
            sum_amount = 0

            if ration_type == 2:
                # 非固定方案
                for i in policy_object_records:
                    sum_premium += i["premium"]
                sum_premium = round(sum_premium, 2)  # 投保标保费累加
                sum_amount = round(sum_premium / premium_rate, 2)  # 保费/标准费率，保留两位小数

            elif ration_type == 1:
                # 固定方案
                sum_premium = round(premium * len(policy_object_records), 2)  # 固定保费*人数
                sum_amount = round(sum_premium/premium_rate, 2) # 总保费/标准费率

            d = DateCal()
            # 根据到签、保险期限、保险期限类型计算投保起止期
            d.insure_date_cal(effect_num, policy_period, policy_period_type)
            insure_start_date = d.start_date
            insure_end_date = d.end_date
            self.expect_insured = {"sumPremium": sum_premium,
                                   "sumAmount": sum_amount,
                                   "insureStartDate": insure_start_date,
                                   "insureEndDate": insure_end_date}
            log.get_log("insurance", "INFO", "锁眼计划-预期保费、保额、保期计算：{}".format(self.expect_insured))
        except Exception as e:
            log.get_log("insurance", "ERROR", "锁眼计划-预期保费、保额、保期计算失败:{}".format(e))

    def get_insured_log(self) -> str:
        """
        请求保司投保mongodb日志提取
        :param:
        :return:
        """
        try:
            url = self.domain_test_mock + self.api_query
            data = self.request_data_query
            water_no = self.res_pre_insured["policy_batch_records"]["waterNo"]
            system_code = self.res_pre_insured["system_config"]["policyChannel"]
            # 组装请求入参
            data["type"] = 3
            data["dev"] = self.dev
            data["taskNo"] = ''
            data["mongoDBCollection"] = system_code + "_policyDownload"
            data["mongoDBKey"] = "originRequest"
            data["mongoDBValue"] = water_no
            # 获取mongoDB日志
            response_data = requests.post(url, headers=self.headers, data=json.dumps(data)).json()
            # 请求保司入参/返参提取
            date_request = response_data["data"]["originRequest"]
            data_response = response_data["data"]["originResponse"]

            # 入参字段值提取
            request_sum_premium = xml_analysis(date_request, "PolicyInfo", "SumPremium")
            request_sum_amount = xml_analysis(date_request, "PolicyInfo", "SumAmount")
            request_start_date = xml_analysis(date_request, "PolicyInfo", "StartDate")
            request_start_time = xml_analysis(date_request, "PolicyInfo", "StartTime")
            request_end_date = xml_analysis(date_request, "PolicyInfo", "EndDate")
            request_end_time = xml_analysis(date_request, "PolicyInfo", "EndTime")
            request_extend_info = xml_analysis(date_request, "ExtendInfos", "ExtendInfo")
            data_request_del = {"SumPremium": request_sum_premium, "SumAmount": request_sum_amount,
                                "StartDate": request_start_date,
                                "StartTime": request_start_time, "EndDate": request_end_date,
                                "end_time": request_end_time,
                                "ExtendInfo": request_extend_info}
            # 返参字段值提取
            response_policy_no = xml_analysis(data_response, "PolicyInfoReturn", "PolicyNo")
            response_download_url = xml_analysis(data_response, "PolicyInfoReturn", "DownloadUrl")
            response_save_result = xml_analysis(data_response, "PolicyInfoReturn", "SaveResult")
            response_sum_premium = xml_analysis(data_response, "PolicyInfoReturn", "SumPremium")
            response_sum_amount = xml_analysis(data_response, "PolicyInfoReturn", "SumAmount")
            data_response_del = {"PolicyNo": response_policy_no, "DownloadUrl": response_download_url,
                                 "SaveResult": response_save_result,
                                 "SumPremium": response_sum_premium, "SumAmount": response_sum_amount}
            self.log_insured = {"insuredRequest": data_request_del, "insuredResponse": data_response_del}
            log.get_log("insurance", "INFO",
                        "提取请求保司-投保mongodb日志-请求保司-投保请求报文:{},请求保司投保返回报文:{}".format(data_request_del, data_response_del))
            return response_data["errno"]
        except Exception as e:
            log.get_log("insurance", "ERROR", "投保mongodb日志字段提取失败:{}".format(e))

    def reset_log(self) -> str:
        """
        清理锁眼计划log表数据
        """
        try:
            request_url = self.domain_test_mock + self.api_action
            request_data = self.request_data_action
            request_data["dev"] = self.dev
            request_data["type"] = 1
            request_data["registNo"] = ""
            response_data = requests.post(request_url, headers=self.headers, data=json.dumps(request_data)).json()
            log.get_log("insurance", "INFO",
                        "-----------清理锁眼计划log表数据,请求地址:{},入参:{},返参:{}----------".format(request_url, request_url,
                                                                                       response_data))
            return response_data["errno"]
        except Exception as e:
            log.get_log("insurance", "ERROR", "清理锁眼计划log表数据失败:{}".format(e))

    def reset_ypb_pool(self, drug_type: int = 0, is_direct_pay: int = 0) -> str:
        """
        释放资金池订单数据-药品保
        :return:
        """
        try:
            request_url = self.domain_test_mock + self.api_mock
            request_data = self.request_data_mock
            request_data["switchConfig"]["orderDataMock"] = 1
            request_data["dev"] = self.dev
            request_data["orderDetail"]["drugType"] = drug_type
            request_data["orderDetail"]["directPay"] = is_direct_pay
            response_data = requests.post(request_url, headers=self.headers, data=json.dumps(request_data)).json()
            log.get_log("insurance", "INFO",
                        "-----------释放资金池订单数据,请求地址:{},入参:{},返参:{}----------".format(request_url, request_data,
                                                                                    response_data))
            return response_data["errno"]
        except Exception as e:
            log.get_log("insurance", "ERROR", "----------释放资金池订单数据失败:{}----------".format(e))

    def do_lock_plan(self, script_key: str) -> (str, bool):
        """
        执行锁眼计划脚本
        :param script_key: 锁眼计划-脚本key
        :return:
        """
        try:
            lock_plan_comm = self.server_config[script_key + "_" + self.dev]
            product_code = lock_plan_comm["productCode"]
            company_name = lock_plan_comm["companyName"]
            env = lock_plan_comm["env"]
            # 拼接脚本命令
            comm = "php console lockPlan --productCode={}  --companyName={}  --env={}".format(product_code,
                                                                                              company_name,
                                                                                              env)
            res = self.server_client.server_comm_execute(comm_list=[comm])
            log.get_log("insurance", "INFO", "----------执行服务器脚本-锁眼计划：{}----------".format(comm))
            do_res = res["data"]["commResult"]
            is_complete = True
            if do_res:
                for i in do_res:
                    # 根据脚本出现"试算异常"字样判断锁眼计划是否执行成功
                    if "试算异常" in i:
                        is_complete = False
                        break
                    else:
                        is_complete = True
            status = res["errno"]
            return status, is_complete
        except Exception as e:
            log.get_log("insurance", "ERROR", "执行服务器脚本-锁眼计划-异常：{}".format(e))

    def get_pool_amount(self) -> any:
        """
        锁眼计划-查询南京资金池日志
        :return:
        """
        try:
            # 获取服务器日志
            res = self.server_client.server_log_read(log_dir="getPoolAmount", read_comm="tail -1")
            # json序列化
            res = json.dumps(res, ensure_ascii=False)
            # 去转义符
            res = res.replace("\\", "")
            # 提取关键内容
            request_data = search('平台请求原始报文：{"body":"' + '{}' + '","headers":', res)
            request_data = json.loads(request_data[0])

            response_data = search('返回报文：' + '{}' + '}",', res)
            response_data = response_data[0] + "}"
            # json反序列化
            response_data = json.loads(response_data)
            # 函数返回处理
            self.log_pool_amount = {"requestData": request_data, "responseData": response_data}
            log.get_log("insurance", "INFO",
                        "-----------查询服务器日志-锁眼计划-查询南京资金池:入参:{},返参:{}----------".format(request_data, response_data))
        except Exception as e:
            log.get_log("insurance", "ERROR", "----------查询服务器日志-锁眼计划-查询南京资金池日志失败:{}----------".format(e))

    def get_policy_task(self) -> any:
        """
        锁眼计划-查询预投保日志
        :return:
        """
        try:
            res = self.server_client.server_log_read(log_dir="policyTask", read_comm="tail -2")
            # json序列化
            res = json.dumps(res, ensure_ascii=False)
            # 去转义符
            res = res.replace("\\", "")
            # 提取关键内容
            request_data = search('平台请求南京原始报文：' + '{}' + '}",', res)
            request_data = request_data[0] + "}"
            request_data = json.loads(request_data)

            response_data = search('policyTask平台请求返回报文：' + '{}' + '}",', res)
            response_data = response_data[0] + "}"
            response_data = json.loads(response_data)
            # 函数返回处理
            self.log_policy_task = {"requestData": request_data, "responseData": response_data}
            log.get_log("insurance", "INFO",
                        "-----------查询预投保日志-锁眼计划-预投保日志:入参:{},返参:{}----------".format(request_data, response_data))
        except Exception as e:
            log.get_log("insurance", "ERROR", "----------查询服务器日志-锁眼计划-预投保日志失败:{}-----------".format(e))


if __name__ == '__main__':
    p = InsureBase('rc')
    # p.reset_drug_order()
    # p.log_reset()
    # p.insure_script_play(script_key="HAIXIA_0")
    # print(p.get_pool_amount_log())
    # print(p.get_policy_task_log())
    # p.get_policy_task()
    # p.cal_except_res()
    a, b = p.do_lock_plan(script_key="HAIXIA_0")
    print(a, b)
    # p.get_policy_task_data('TB220726005')
    # p.get_pool_result_data('TB220726005')
    # p.insure_data_cal()
    # p.mongo_insure_log_get()
    # print(p.insured_res, p.insure_cal, p.data_policy_task, p.data_policy_result)
    # a = p.insure_data_cal()
    # print(a)
