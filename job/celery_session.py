from typing import List
from schems.policy.common import *
from extensions.logger import log
import requests


def session_post(param_list: List[SessionParameter]):
    """
    批量处理请求
    :param param_list:
    :return:
    """
    header = {"Content-Type": "application/json"}
    for i in param_list:
        log.get_log(
            "celery_task", "INFO", "API:{}".format(i.url)
        )
        log.get_log(
            "celery_task", "INFO", "入参:{}".format(i.body)
        )
        r = requests.post(i.url, data=i.body, headers=header).json()
        log.get_log(
            "celery_task", "INFO", "返参:{}".format(r)
        )




