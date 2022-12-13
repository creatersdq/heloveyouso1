import os
import time
import unittest
import allure
import parameterized
import json
import pytest

from apps.ui.core.config import BASE_DIR
from apps.ui.page.login import LoginProxy
from apps.ui.core.utils import DriverUtil


def build_data():
    """
    测试数据初始化
    """
    test_data = []
    # 1.通过方法或者函数读取json数据
    with open(BASE_DIR + '/data/test_login.json', encoding='utf-8') as f:
        json_data = json.load(f)
        # 2.将读取回来的数据组装成parameterized所要求的数据格式
        for case_data in json_data.values():
            test_data.append((case_data.get('username'),
                              case_data.get('password'),
                              case_data.get('expect')))
    return test_data


class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with allure.step("启动浏览器"):
            # 创建浏览器驱动，并且完成初始化操作
            cls.driver = DriverUtil.get_driver()
            cls.login_proxy = LoginProxy()

    @classmethod
    def tearDownClass(cls):
        with allure.step("关闭浏览器"):
            time.sleep(2)
            DriverUtil.quit_driver()

    def setUp(self):
        with allure.step("打开登录页面"):
            login_url = "http://frontend-insurance-platform.turboradio.cn/login"
            # 登录页面
            self.driver.get(login_url)

    # 数据驱动参数化
    # parameterized中的数据是一个数组，数组内的每个元素可以数组或者元组，

    @parameterized.parameterized.expand(build_data)
    @allure.feature("药联慧保")
    @allure.story("登录")
    @allure.title("登录成功")
    def test_login(self, username, password, expect):
        with allure.step("登录"):
            self.login_proxy.login(username, password)
        with allure.step("固定等待时间-3s"):
            time.sleep(3)
        with allure.step("断言-是否登录成功"):
            msg = self.driver.title
            self.assertIn(expect, msg)


if __name__ == "__main__":
    pytest.main(['-s', '-q', './test_login.py', '--clean-alluredir', '--alluredir=allure-results'])
    os.system(r"allure generate -c -o allure-report")
    # pytest.main()
    # os.system(r"allure generate -c -o ./allure_report")
    # build_data()
    # pytest.main([
    #     './'
    #     '/test_login.py',
    #     "--alluredir=./"
    #     "/test_cases"
    #     "/allure_results"])
    # # # 生成测试报告
    # os.system(
    #     r"allure generate ./"
    #     r"/cases/allure_results -o "
    #     r"./"
    #     r"/allure_report")
