# TestLoader
# 导包
import time
import unittest
from HTMLTestRunner import HTMLTestRunner
from apps.ui.core.config import BASE_DIR

# 设置浏览器驱动关闭开关为False
# DriverUtil.is_open = False

# 生成测试套件
suite = unittest.TestLoader().discover('./cases', 'test*')
# 定义测试报告路径
report_path = BASE_DIR + "/report/report-{}.html".format(time.strftime("%Y%m%d%H%M%S"))

if __name__ == "__main__":
    with open(report_path, "w") as f:
        # 实例化运行器
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='测试报告', description="firefox")
        # 运行测试用例
        runner.run(suite)


# 打开关闭浏览器开关，并关闭浏览器
# DriverUtil.is_open = True
# DriverUtil.quit_dirver()
