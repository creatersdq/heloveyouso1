import requests

from typing import List
from model.session import Param
from extension.logger import log


def session_post(param_list: List[Param]):
    """
    批量处理请求
    :param param_list:
    :return:
    """
    header = {"Content-Type": "application/json"}
    for i in param_list:
        log.get_log(
            "job", "INFO", "API:{}".format(i.url)
        )
        log.get_log(
            "job", "INFO", "入参:{}".format(i.body)
        )
        r = requests.post(i.url, data=i.body, headers=header).json()
        log.get_log(
            "job", "INFO", "返参:{}".format(r)
        )
