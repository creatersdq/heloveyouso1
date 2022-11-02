import allure

from apps import log
from apps.cases.Insurance_interconnection.insure import InsureBase


class InsuranceCaseBase(object):
    def __init__(self):
        self.insured_except_data = {}  # 预期投保数据
        self.insured_request_data = {}  # 实际投保入参
        self.insured_response_data = {}  # 实际投保返参
        self.insured_res = {}  # 投保结果入表
        self.task_no = None  # 投保单号

    def save_cases_res(self):
        pass

    def lock_plan_play(self, insure_base: InsureBase, script_name: str) -> any:
        """
        执行锁眼计划
        :param insure_base:
        :param script_name: 锁眼计划脚本名
        :return:
        """
        # 读取脚本配置
        config = insure_base.server_config[script_name + "_" + insure_base.dev]
        drug_type = config["drugType"]
        is_direct_pay = config["iDirectPay"]
        latitude = config["latitude"]

        with allure.step("清理锁眼计划日志表"):
            status = insure_base.reset_log()
            assert status == "0"

        with allure.step("根据药品类型-释放资金池订单数据"):
            # 根据药品类型释放资金池
            status = insure_base.reset_ypb_pool(drug_type=drug_type, is_direct_pay=is_direct_pay)
            assert status == "0"
        with allure.step("执行锁眼计划脚本:{}".format(script_name)):
            status, is_complete = insure_base.do_lock_plan(script_key=script_name)
            assert status == "0"
            assert is_complete is True
        with allure.step("查询资金池可投金额"):
            insure_base.get_pool_amount()  # 获取查询资金池服务器日志
        with allure.step("预投保"):
            insure_base.get_policy_task()  # 获取预投保服务器日志
            self.task_no = insure_base.log_policy_task["requestData"]["taskNo"]  # 提取投保单号
            assert self.task_no is not None
        with allure.step("预投保回调-投保单号:{}".format(self.task_no)):
            status = insure_base.get_pre_insured(self.task_no)  # 获取预投保关联表数据
            assert status == "0"
            task_status = insure_base.res_pre_insured["policy_batch_records"]["systemStatus"]  # 实时提取投保单状态
            assert task_status == 6
        with allure.step("预期结果计算：保费、保额、保期"):
            insure_base.cal_except_res()
            except_data = insure_base.expect_insured
            # 断言字段提取
            self.insured_except_data["SumPremium"] = float(except_data["sumPremium"])  # 预期保费
            self.insured_except_data["SumAmount"] = float(except_data["sumAmount"])  # 预期保额
            self.insured_except_data["StartDate"] = str(except_data["insureStartDate"])  # 预期保险起期
            self.insured_except_data["EndDate"] = str(except_data["insureEndDate"])  # 预期保险止期
            log.get_log("insurance", "INFO", "投保预期值计算：保费:{},保额:{},保险起期:{},保险止期:{}".format(
                self.insured_except_data["SumPremium"],
                self.insured_except_data["SumAmount"],
                self.insured_except_data["StartDate"],
                self.insured_except_data["EndDate"]))
        with allure.step("请求保司节点"):
            status = insure_base.get_insured_log()  # 获取请求保司投保接口mongoDB日志
            assert status == "0"
            actual_insured_data = insure_base.log_insured
            assert actual_insured_data is not None
            self.insured_request_data["SumPremium"] = float(
                actual_insured_data["insuredRequest"]["SumPremium"])  # 实际投保保费
            self.insured_request_data["SumAmount"] = float(
                actual_insured_data["insuredRequest"]["SumAmount"])  # 实际投保保额
            self.insured_request_data["StartDate"] = actual_insured_data["insuredRequest"][
                                                         "StartDate"] + " " + \
                                                     actual_insured_data["insuredRequest"][
                                                         "StartTime"]  # 实际投保保险起期
            self.insured_request_data["EndDate"] = actual_insured_data["insuredRequest"][
                                                       "EndDate"] + " " + \
                                                   actual_insured_data["insuredRequest"][
                                                       "end_time"]  # 实际投保止期
            self.insured_request_data["ExtendInfo"] = actual_insured_data["insuredRequest"][
                "ExtendInfo"]  # 实际投保文件
            log.get_log("insurance", "INFO", "实际投保相关字段获取：保费:{},保额:{},保险起期:{},保险止期:{},电子保单地址:{}".format(
                self.insured_request_data["SumPremium"],
                self.insured_request_data["SumAmount"],
                self.insured_request_data["StartDate"],
                self.insured_request_data["EndDate"],
                self.insured_request_data["ExtendInfo"]))
            if actual_insured_data["insuredResponse"]["PolicyNo"]:
                self.insured_response_data["PolicyNo"] = actual_insured_data["insuredResponse"][
                    "PolicyNo"]  # 保司返回投保单号
            if actual_insured_data["insuredResponse"]["DownloadUrl"]:
                self.insured_response_data["DownloadUrl"] = actual_insured_data["insuredResponse"][
                    "DownloadUrl"]  # 电子保单地址
            if actual_insured_data["insuredResponse"]["SaveResult"]:
                self.insured_response_data["SaveResult"] = actual_insured_data["insuredResponse"][
                    "SaveResult"]  # 投保状态码
            if actual_insured_data["insuredResponse"]["SumPremium"]:
                self.insured_response_data["SumPremium"] = actual_insured_data["insuredResponse"][
                    "SumPremium"]  # 保司返回保费
            if actual_insured_data["insuredResponse"]["SumAmount"]:
                self.insured_response_data["sumAmount"] = actual_insured_data["insuredResponse"][
                    "SumAmount"]  # 保司返回保额
            log.get_log("insurance", "INFO",
                        "保司投保接口返回：保单号:{},电子保单下载地址:{},投保结果状态码:{},保费:{},""保额:{}".format(
                            self.insured_response_data["PolicyNo"],
                            self.insured_response_data["DownloadUrl"],
                            self.insured_response_data["SaveResult"],
                            self.insured_response_data["SumPremium"],
                            self.insured_response_data["sumAmount"]))
        with allure.step("保存投保结果-保单号:{}".format(self.insured_response_data["PolicyNo"])):
            status = insure_base.get_actual_insured(self.task_no)  # 获取投保结果关联表数据
            assert status == "0"
            actual_data = insure_base.res_actual_insured
            assert actual_data is not None
            if actual_data["policy_records"]["policyNo"]:
                self.insured_res["policyNo"] = str(
                    actual_data["policy_records"]["policyNo"])  # policy_records.policyNo
            if actual_data["policy_records"]["sumPremium"]:
                self.insured_res["sumPremium"] = str(
                    actual_data["policy_records"]["sumPremium"])  # policy_records.sumPremium
            if actual_data["policy_records"]["sumAmount"]:
                self.insured_res["sumAmount"] = str(
                    actual_data["policy_records"]["sumAmount"])  # policy_records.sumAmount
            if actual_data["policy_file_records"]["epolicyUrl"]:
                self.insured_res["epolicyUrl"] = str(
                    actual_data["policy_file_records"]["epolicyUrl"])  # policy_records.ossEpolicyUrl
            log.get_log("insurance", "INFO", "投保结束入表数据提取:保单号:{},保费:{},保额:{},电子保单下载地址:{}".format(
                self.insured_res["policyNo"],
                self.insured_res["sumPremium"],
                self.insured_res["sumAmount"],
                self.insured_res["epolicyUrl"]))

    def do_claim(self):
        pass

    def do_claim_tem(self):
        pass
