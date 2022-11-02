import os
import pytest
import allure

from apps.cases.Insurance_interconnection.base import InsureBase, InsuranceCaseBase

# 环境
case_dev = 'rc'
# 实例化
insure_base = InsureBase(dev=case_dev)
case_base = InsuranceCaseBase()


class TestLockPlanOnline(object):
    """
    线上投保
    """

    @pytest.mark.skip(reason="跳过，档位制暂不支持")
    @allure.feature("锁眼计划")
    @allure.story("天安")
    @allure.title("TIANAN_0-特药直赔-寿险-档位制")
    def test_tianan_0(self):
        case_name = 'TIANAN_0'
        # 执行锁眼计划
        case_base.lock_plan_play(insure_base, script_name=case_name)
        # 断言
        with allure.step("请求保司入参保费/保额/保期断言"):
            assert case_base.insured_except_data["SumPremium"] - case_base.insured_request_data["SumPremium"] == 0
            assert case_base.insured_except_data["SumAmount"] - case_base.insured_request_data["SumAmount"] == 0
            assert case_base.insured_except_data["StartDate"] == case_base.insured_request_data["StartDate"]
            assert case_base.insured_except_data["EndDate"] == case_base.insured_request_data["EndDate"]
        with allure.step("投保结果入表数据断言"):
            assert case_base.insured_response_data["PolicyNo"] == case_base.insured_res["PolicyNo"]
            assert case_base.insured_response_data["DownloadUrl"] == case_base.insured_res["epolicyUrl"]

    @allure.feature("锁眼计划")
    @allure.story("紫金财险")
    @allure.title("ZIJIN_0-普药直赔-寿险")
    def test_zijin_0(self):
        case_name = 'ZIJIN_0'
        # 执行锁眼计划
        case_base.lock_plan_play(insure_base, script_name=case_name)
        # 断言
        with allure.step("请求保司入参保费/保额/保期断言"):
            assert case_base.insured_except_data["SumPremium"] - case_base.insured_request_data["SumPremium"] == 0
            assert case_base.insured_except_data["SumAmount"] - case_base.insured_request_data["SumAmount"] == 0
            assert case_base.insured_except_data["StartDate"] == case_base.insured_request_data["StartDate"]
            assert case_base.insured_except_data["EndDate"] == case_base.insured_request_data["EndDate"]
        with allure.step("投保结果入表数据断言"):
            assert case_base.insured_response_data["PolicyNo"] == case_base.insured_res["policyNo"]
            assert case_base.insured_response_data["DownloadUrl"] == case_base.insured_res["epolicyUrl"]

    @allure.feature("锁眼计划")
    @allure.story("紫金财险")
    @allure.title("ZIJIN_1-普药直赔-寿险")
    def test_zijin_1(self):
        case_name = 'ZIJIN_1'
        # 执行锁眼计划
        case_base.lock_plan_play(insure_base, script_name=case_name)
        # 断言
        with allure.step("请求保司入参保费/保额/保期断言"):
            assert case_base.insured_except_data["SumPremium"] - case_base.insured_request_data["SumPremium"] == 0
            assert case_base.insured_except_data["SumAmount"] - case_base.insured_request_data["SumAmount"] == 0
            assert case_base.insured_except_data["StartDate"] == case_base.insured_request_data["StartDate"]
            assert case_base.insured_except_data["EndDate"] == case_base.insured_request_data["EndDate"]
        with allure.step("投保结果入表数据断言"):
            assert case_base.insured_response_data["PolicyNo"] == case_base.insured_res["policyNo"]
            assert case_base.insured_response_data["DownloadUrl"] == case_base.insured_res["epolicyUrl"]

    @pytest.mark.skip(reason="跳过-需配置ip白名单")
    @allure.feature("锁眼计划")
    @allure.story("中路")
    @allure.title("ZHONGLU_0-普药直赔-寿险")
    def test_zhonglu_0(self):
        case_name = 'ZHONGLU_0'
        # 执行锁眼计划
        case_base.lock_plan_play(insure_base, script_name=case_name)
        # 断言
        with allure.step("请求保司入参保费/保额/保期断言"):
            assert case_base.insured_except_data["SumPremium"] - case_base.insured_request_data["SumPremium"] == 0
            assert case_base.insured_except_data["SumAmount"] - case_base.insured_request_data["SumAmount"] == 0
            assert case_base.insured_except_data["StartDate"] == case_base.insured_request_data["StartDate"]
            assert case_base.insured_except_data["EndDate"] == case_base.insured_request_data["EndDate"]
        with allure.step("投保结果入表数据断言"):
            assert case_base.insured_response_data["PolicyNo"] == case_base.insured_res["policyNo"]
            assert case_base.insured_response_data["DownloadUrl"] == case_base.insured_res["epolicyUrl"]

    @allure.feature("锁眼计划")
    @allure.story("海峡")
    @allure.title("HAIXIA_0-普药非直赔-寿险")
    def test_haixia_0(self):
        case_name = 'HAIXIA_0'
        # 执行锁眼计划
        case_base.lock_plan_play(insure_base, script_name=case_name)
        # 断言
        with allure.step("请求保司入参保费/保额/保期断言"):
            assert case_base.insured_except_data["SumPremium"] - case_base.insured_request_data["SumPremium"] == 0
            assert case_base.insured_except_data["SumAmount"] - case_base.insured_request_data["SumAmount"] == 0
            assert case_base.insured_except_data["StartDate"] == case_base.insured_request_data["StartDate"]
            assert case_base.insured_except_data["EndDate"] == case_base.insured_request_data["EndDate"]
        with allure.step("投保结果入表数据断言"):
            assert case_base.insured_response_data["PolicyNo"] == case_base.insured_res["policyNo"]
            # assert case_base.insured_response_data["DownloadUrl"] == case_base.insured_res["epolicyUrl"]

    @pytest.mark.skip(reason="跳过-保司接口暂时不通")
    @allure.feature("锁眼计划")
    @allure.story("长江")
    @allure.title("CHANGJIANG_0-普药非直赔-财险-档位制")
    def test_changjiang(self):
        case_name = 'CHANGJIANG_0'
        # 执行锁眼计划
        case_base.lock_plan_play(insure_base, script_name=case_name)
        # 断言
        with allure.step("请求保司入参保费/保额/保期断言"):
            assert case_base.insured_except_data["SumPremium"] - case_base.insured_request_data["SumPremium"] == 0
            assert case_base.insured_except_data["SumAmount"] - case_base.insured_request_data["SumAmount"] == 0
            assert case_base.insured_except_data["StartDate"] == case_base.insured_request_data["StartDate"]
            assert case_base.insured_except_data["EndDate"] == case_base.insured_request_data["EndDate"]
        with allure.step("投保结果入表数据断言"):
            assert case_base.insured_response_data["PolicyNo"] == case_base.insured_res["policyNo"]
            assert case_base.insured_response_data["DownloadUrl"] == case_base.insured_res["epolicyUrl"]

    @pytest.mark.skip(reason="跳过-保司接口暂时不通")
    @allure.feature("锁眼计划")
    @allure.story("众诚")
    @allure.title("ZHONGCHENG_0-普药非直赔-寿险")
    def test_zhongcheng_0(self):
        case_name = 'ZHONGCHENG_0'
        # 执行锁眼计划
        case_base.lock_plan_play(insure_base, script_name=case_name)
        # 断言
        with allure.step("请求保司入参保费/保额/保期断言"):
            assert case_base.insured_except_data["SumPremium"] - case_base.insured_request_data["SumPremium"] == 0
            assert case_base.insured_except_data["SumAmount"] - case_base.insured_request_data["SumAmount"] == 0
            assert case_base.insured_except_data["StartDate"] == case_base.insured_request_data["StartDate"]
            assert case_base.insured_except_data["EndDate"] == case_base.insured_request_data["EndDate"]
        with allure.step("投保结果入表数据断言"):
            assert case_base.insured_response_data["PolicyNo"] == case_base.insured_res["policyNo"]
            assert case_base.insured_response_data["DownloadUrl"] == case_base.insured_res["epolicyUrl"]

    @allure.feature("锁眼计划")
    @allure.story("国任")
    @allure.title("GUOREN_0普药非直赔-寿险")
    def test_guoren_0(self):
        pass

    @allure.feature("锁眼计划")
    @allure.story("国任")
    @allure.title("GUOREN_1-普药非直赔-寿险")
    def test_guoren_1(self):
        pass

    @allure.feature("锁眼计划")
    @allure.story("国任")
    @allure.title("GUOREN_2-普药非直赔-寿险")
    def test_guoren_2(self):
        pass


if __name__ == '__main__':

    pytest.main([
        '/Users/uniondrug/Desktop/qtest1006/quality.autotest/apps/cases/Insurance_interconnection/test_cases'
        '/test_insure_online.py',
        "--alluredir=/Users/uniondrug/Desktop/qtest1006/quality.autotest/apps/cases/Insurance_interconnection"
        "/test_cases"
        "/allure_results"])
    # 生成测试报告
    os.system(
        r"allure generate /Users/uniondrug/Desktop/qtest1006/quality.autotest/apps/cases/Insurance_interconnection"
        r"/test_cases/allure_results -o "
        r"/Users/uniondrug/Desktop/qtest1006/quality.autotest/apps/cases/Insurance_interconnection/test_cases"
        r"/allure_report")
