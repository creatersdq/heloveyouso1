import os, sys
import requests, json
# import pytest
import subprocess
import datetime


# 启动多线程or多进程执行脚本需注意，执行脚本进程数和线程数需小于项目启动进程，线程数
# ProcessWork 开启任务执行进程数
# ThreadWork 开启任务执行线程数
def start_up1(case_path, process_work=1, thread_work=1):
    html_dir = datetime.datetime.now().strftime('%Y-%m-%d')
    sys.path.append(os.path.dirname(sys.modules[__name__].__file__))
    path = os.path.dirname(os.path.abspath(__file__))
    case_dir = path + '/automaticTest/CasePath'
    report_dir  = path + '/report/{}/{}'.format(case_path, html_dir)
    if os.path.exists(path + '/report/{}/{}'.format(case_path, html_dir)):
        pass
    else:
        os.makedirs(path + '/report/{}/{}'.format(case_path, html_dir))

    try:
        subprocess.getstatusoutput(
            ' pytest {} --workers={} --tests-per-worker={}  '
            '--html={}.html'.format(case_dir, process_work, thread_work, report_dir))
        pass
    except:
        pass



def start_up(case_path=None):

    subprocess.getstatusoutput(
        ' pytest {}  --html={}'.format("/Users/living/PycharmProjects/DockerProject/quality.autotest/apps/unitst/ujl.py",
                                "/data/report/a.html"))

# start_up()
# print(os.path.dirname(os.path.dirname(__file__)))