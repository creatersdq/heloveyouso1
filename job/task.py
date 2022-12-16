import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import time
from model.policy.common import *
from job.celery_app import app
from job.celery_session import session_post


@app.task
def add(x, y):
    time.sleep(30)
    return x + y


@app.task
def post(request_list: list):
    """
    批量处理post请求
    :param request_list:
    :return:
    """
    a = SessionParameter()
    e_list = []
    for i in request_list:
        a.url = i["url"]
        a.body = i["body"]
        e_list.append(a)
    session_post(e_list)
    return "done"
