import json
import requests

from apps.extensions.logger import log
from apps.cases.common.insurance_common.cases_config import common_config, server_config


class ServerBase(object):

    def __init__(self, dev: str, entry_name: str):
        """

        :param dev: 环境
        :param entry_name: 连接项目名称，取redis配置
        """
        self.domain_test_mock = common_config["COMMON_DOMAIN_NAME_RC"]["TEST_MOCK"]
        self.api_server_handle = common_config["API"]["POLICY_SERVER_HANDLE"]
        self.headers = {"Content-Type": "application/json"}
        self.entry_name = entry_name
        self.dev = dev

    def server_comm_execute(self, comm_list: list) -> dict:
        """
        执行服务器命令
        :param comm_list:脚本命令
        :return:
        """
        # 接口地址
        request_url = self.domain_test_mock + self.api_server_handle
        # 组装请求入参
        server_detail = {"entryName": self.entry_name, "commList": comm_list, "dev": self.dev}
        request_data = {"serverDetail": server_detail}
        # 请求服务器连接接口
        res = requests.post(request_url, headers=self.headers, data=json.dumps(request_data)).json()
        # 返参数据提取
        return res

    def server_log_read(self, log_dir: str, read_comm: str) -> list:
        """

        :param log_dir: 读取日志文件名
        :param read_comm: 读取linux命令，cat/tail
        :return:
        """
        # 接口地址
        request_url = self.domain_test_mock + self.api_server_handle
        # 组装请求入参
        server_detail = {"entryName": self.entry_name, "commList": [], "dev": self.dev}
        server_log_detail = {"serverDirName": log_dir, "daysRetrospective": 0, "readComm": read_comm}
        request_data = {"serverDetail": server_detail, "serverLogDetail": server_log_detail}
        # 请求服务器连接接口
        res = requests.post(request_url, headers=self.headers, data=json.dumps(request_data)).json()
        # 返参数据提取
        res = res["data"]["commResult"]
        return res


if __name__ == '__main__':
    s = ServerBase(dev='rc', entry_name='module_equity_claim')
    a = s.server_comm_execute(["pwd"])
    print(a)
    print(type(a))
    b = s.server_log_read(log_dir="getPoolAmount", read_comm="cat")
    print(b)
    print(type(b))
