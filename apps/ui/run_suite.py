# TestLoader
# 导包
import os
import time
import unittest

import pytest
from HTMLTestRunner import HTMLTestRunner
from apps.ui.core.config import BASE_DIR

# 设置浏览器驱动关闭开关为False
# DriverUtil.is_open = False

# 生成测试套件
suite = unittest.TestLoader().discover('./cases', 'test*')
# 定义测试报告路径
report_path = BASE_DIR + "/report/report-{}.html".format(time.strftime("%Y%m%d%H%M%S"))

if __name__ == "__main__":
    # 项目根目录
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 执行测试用例目录
    case_dir = "%s/cases" % BASE_DIR
    # allure测试结果存放路径
    allure_result_dir = "--alluredir=%s/allure_results" % BASE_DIR
    allure_report_dir = "%s/allure_report" % BASE_DIR
    print(case_dir, allure_result_dir, allure_report_dir)
    # pytest.main()
    # pytest.main(['-s', '-q', case_dir, '--clean-alluredir', allure_result_dir])
    # pytest.main(['-s', '-q', "./cases", '--clean-alluredir', 'alluredir="allure_result"'])
    # os.system(r"allure generate -c -o allure_report")
    pytest.main(['-s', '-q', './cases', '--clean-alluredir', '--alluredir=./allure-results'])
    os.system(r"allure generate -c -o ./allure-report")
    # with open(report_path, "w") as f:
    #     # 实例化运行器
    #     runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='测试报告', description="firefox")
    #     # 运行测试用例
    #     runner.run(suite)

# 打开关闭浏览器开关，并关闭浏览器
# DriverUtil.is_open = True
# DriverUtil.quit_dirver()
