import time
import unittest
import parameterized as parameterized
from apps.ui_auto.core.config import BASE_DIR
from apps.ui_auto.page.login_page import LoginProxy
from apps.ui_auto.core.utils import DriverUtil
import json


def build_data():
    test_data = []
    # 1.通过方法或者函数读取json数据
    with open(BASE_DIR + '/data/test_login.json', encoding='utf-8')as f:
        json_data = json.load(f)
        # 2.将读取回来的数据组装成parameterized所要求的数据格式
        for case_data in json_data.values():
            test_data.append((case_data.get('username'),
                              case_data.get('password'),
                              case_data.get('expect')))
            print(test_data)
    return test_data


class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 创建浏览器驱动，并且完成初始化操作
        cls.driver = DriverUtil.get_driver()
        cls.login_proxy = LoginProxy()

    @classmethod
    def tearDownClass(cls):
        # 关闭浏览器
        time.sleep(2)
        DriverUtil.quit_dirver()

    def setUp(self):
        # 方法级别的fixture，由于每条测试都要回归到原点
        self.driver.get('https://ad.xxx.com.cn/home')

    # parameterized中的数据是一个数组，数组内的每个元素可以数组或者元组
    @parameterized.expand(build_data)
    def test_login(self, username, password, expect):
        """
        登录功能-登录成功
        """
        self.login_proxy.login(username, password)
        # 获取提示信息
        time.sleep(3)
        msg = self.driver.title
        self.assertIn(expect, msg)
