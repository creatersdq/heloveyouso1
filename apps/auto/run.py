import json

from requests import request
import datetime
import os
import time
import pytest
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from apps.db_actions.common_case import statistics_history_data
from apps.core.conf import setting


def run_enter(project_name):
    """project_name 要运行的项目名"""
    base_dir = os.getcwd()
    project_madir = base_dir + '/cases'
    project_name_list = os.listdir(project_madir)
    project_name_list.pop(project_name_list.index('__init__.py'))
    project_name_list.pop(project_name_list.index('common'))
    project_name_list.pop(project_name_list.index('conftest.py'))
    # 判断传入的项目是否在当前cases中，如果不存在，直接返回"项目名称错误"
    if project_name not in project_name_list:
        return "项目名字错误"

    # 供数据库统计用例执行情况，value值作为project_name条件使用
    project_names = {
        "logistics": '物流项目',
        "promotecenter": "营销中心",
        "equitys": "权益中心"
    }
    name = project_names[project_name]
    now_time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    file_name = project_name + "_" + now_time_str
    # 运行pytest用例
    pytest.main(['cases/{}/test_cases'.format(project_name),
                 "--alluredir=/data/report/{}/{}/allure_results".format(project_name,
                                                                        file_name)])
    os.system(
        r"allure generate /data/report/{}/{}/allure_results -o /data/report/{}/{}/allure_report".format(
            project_name,
            file_name,
            project_name,
            file_name))
    # # 部署后使用
    dingding_data_dir = "/data/report/" + project_name + "/" + \
                        file_name + "/" + "allure_report/widgets/history-trend.json"
    executors_data_dir = "/data/report/" + project_name + '/' + \
                         file_name + '/' + "allure_report/widgets/executors.json"

    # 本地调试使用
    # dingding_data_dir = base_dir + "/data/report/" + project_name + '/' + \
    #                     file_name + '/' + "allure_report/widgets/history-trend.json"
    # executors_data_dir = base_dir + "/data/report/" + project_name + '/' + \
    #                      file_name + '/' + "allure_report/widgets/executors.json"
    with open(dingding_data_dir, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
        present_data = json_data[0]["data"]
    case_total = present_data['total']
    pass_count = present_data['passed']
    fail_count = present_data['failed']
    trouble_count = present_data['broken']
    if fail_count == 0 and trouble_count == 0:
        test_result = 'PASS'
    else:
        test_result = "FAILED"

    history_data = statistics_history_data(project_name)
    list_data = []

    for i in history_data:
        x = {
            "data": {
                "failed": None,
                "broken": 0,
                "skipped": 0,
                "passed": None,
                "unknown": 0,
                "total": None}}
        x["data"]["total"] = i[0]
        x["data"]["passed"] = i[1]
        x["data"]["failed"] = i[2]
        list_data.append(x)

    with open(dingding_data_dir, 'w', encoding="utf-8") as f:
        json.dump(list_data, f)

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

    with open(executors_data_dir, 'w', encoding='utf-8') as ef:
        ef.write(json.dumps(executors_data))
    # index.html文件路径
    index_dir = "/" + project_name + '/' + \
                file_name + '/allure_report' + '/index.html'

    report_address = "http://" + 'test-report.uniondrug.net' + index_dir
    env = setting()['ENV']
    url = 'http://opentest-backend.uniondrug.net/api/send/testResult'
    data = {
        "projectName": name,
        "caseTotal": case_total,
        "passCount": pass_count,
        "failCount": fail_count,
        "testResult": test_result,
        "reportAddress": report_address,
        "env": env,
        "breakCount": trouble_count
    }
    # 请求临时钉钉接口
    request(method="POST", url=url, json=data)


if __name__ == '__main__':
    project_name = 'logistics'
    run_enter(project_name)