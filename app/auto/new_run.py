import json

from requests import request
import os
import time
import pytest
import sys
from apps.db_actions.case_run_actions import update_test_plan

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from apps.db_actions.common_case import his_trend_data
from apps.core.conf import setting


def run_case(prj: str = None,  plan_no: str = None):
    # 判断prj是否已完成case自动化编写
    base_dir = os.getcwd()
    if prj in ['__init__.py', 'common', 'conftest.py', '__pycache__'] or prj not in os.listdir(base_dir + '/cases'):
        return "项目不存在"
    now_time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    file_name = prj + "_" + now_time_str
    # 新增路径判断
    if setting()['ENV'] == "TEST":
        report_dir = base_dir
    else:
        report_dir = ""
    # 执行测试用例
    pytest.main(['{}/cases/{}/test_cases'.format(base_dir, prj), "--cmdopt={}".format(plan_no),
                 # "--report-log={}/log/sys_run/{}.json".format(base_dir, file_name),
                 "--alluredir={}/data/report/{}/{}/allure_results".format(report_dir, prj, file_name)])
    # 生成测试报告
    os.system(
        r"allure generate {}/data/report/{}/{}/allure_results -o {}/data/report/{}/{}/allure_report".format(
            report_dir, prj, file_name, report_dir, prj, file_name))

    # 测试结果通知
    history_trend_path = report_dir + '/data/report/' + prj + "/" + file_name + "/" + "allure_report/widgets/history-trend.json"
    # 运行器
    executors_path = report_dir + '/data/report/' + prj + '/' + file_name + '/' + "allure_report/widgets/executors.json"
    # 补充历史趋势统计数据
    his_trend = his_trend_data(prj)
    list_data = []
    for i in his_trend:
        x = {
            "data": {"failed": None, "broken": 0, "skipped": 0, "passed": None, "unknown": 0, "total": None}
        }
        x["data"]["total"] = i[1]
        x["data"]["passed"] = i[2]
        x["data"]["failed"] = i[3]
        x["data"]["broken"] = i[4]
        x["data"]["skipped"] = i[5]
        x["data"]["unknown"] = i[6]
        list_data.append(x)
    with open(history_trend_path, 'r+', encoding="utf-8") as f:
        f.truncate()
        json.dump(list_data, f)
    # 报告运行器
    executors_data = [{
        "name": "技术运营部-质量验收组",
        "type": "api",
        "url": "",
        "buildOrder": "9527",
        "buildName": "测试平台",
        "buildUrl": "http://front-opentest.uniondrug.net",
        "reportName": "自动化测试",
        "reportUrl": ""
    }]

    with open(executors_path, 'w+', encoding='utf-8') as ef:
        ef.write(json.dumps(executors_data))
    # index.html文件路径
    index_dir = "/" + prj + '/' + file_name + '/allure_report' + '/index.html'
    report_address = "http://" + "test-report.uniondrug.net" + index_dir
    # 如果不存在历史记录，则不发起钉钉消息推送（默认判断为测试时候调试）
    if his_trend:
        # 报告同步至库
        update_test_plan(plan_no, report_address)
        env = setting()['ENV']
        url = 'http://opentest-backend.uniondrug.net/api/send/testResult'
        data = {
            "projectName": prj,
            "caseTotal": his_trend[0][1],
            "passCount": his_trend[0][2],
            "failCount": his_trend[0][3],
            "testResult": 'PASS' if his_trend[0][1] == his_trend[0][2] else "FAILED",
            "reportAddress": report_address,
            "env": env,
            "breakCount": his_trend[0][3]
        }
        # 请求临时钉钉接口
        request(method="POST", url=url, json=data)


if __name__ == '__main__':
    run_case("ddd", "ddddd")
