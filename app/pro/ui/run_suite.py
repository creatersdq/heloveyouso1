# TestLoader
# 导包
import os
import time
import unittest

import pytest
from app.pro.ui.core.config import BASE_DIR

# 设置浏览器驱动关闭开关为False
# DriverUtil.is_open = False

# 生成测试套件
suite = unittest.TestLoader().discover('cases', 'test*')
# 定义测试报告路径
report_path = BASE_DIR + "/report/report-{}.html".format(time.strftime("%Y%m%d%H%M%S"))

if __name__ == "__main__":
    # 项目根目录
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 执行测试用例目录
    case_dir = "%s/cases" % BASE_DIR

    # 定义 测试结果&测试报告&执行用例目录
    allure_result_dir = "allure_results"
    allure_report_dir = "allure_report"
    cases_dir = 'cases'
    # 获取当前日期
    times = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    pytest.main(['-s', '-q', cases_dir, '--clean-alluredir', '--alluredir=%s' % allure_result_dir])
    # 生成测试报告
    os.system("allure generate %s -o %s/report_%s --clean" % (allure_result_dir, allure_report_dir, times))

    """
    生成测试报告
    allure generate -c -o ./allure-report  --clean
    每次生成报告不替换之前的
    allure generate -c -o ./allure-report/report_'+times+' --clean
    """
