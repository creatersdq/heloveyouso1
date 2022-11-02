import datetime
import json
import os
import re

from sh import ssh
from app.curd.curd_redis import redis_query
from app.extensions.logger import log
from app.extensions.random_number import StochasticNum


class Server_Sh(object):
    def __init__(
            self,
            entry_name: str,
            dev: str
    ):
        """
        :param entry_name: 项目名，redis配置
        :param dev: 环境：测试，rc
        """
        # 目标主机
        self.config = json.loads(redis_query(name='cn_ud_test_mock')["server_config"])[entry_name + "_" + dev]
        self.host_name = self.config["SERVER_HOSTNAME"]
        self.port = self.config["SERVER_PORT"]
        self.user_name = self.config["SERVER_USERNAME"]
        self.entry_path = self.config["PATH"]
        self.cd_entry_path_comm = "cd " + self.config["PATH"]

        # 服务器日志路径
        self.server_task_log_dir = ''
        self.server_task_no = ''

    def send(
            self,
            comm_list: list
    ) -> any:
        """
        执行服务器命令
        :param comm_list:
        :return:
        """
        # 定义日志路径
        day = str(datetime.datetime.now().strftime("/%Y-%m/%Y-%m-%d/"))
        # 自定义任务编号
        self.server_task_no = StochasticNum().water_no("serverTask")
        # 拼接日志路径
        self.server_task_log_dir = "serverTask" + day + self.server_task_no
        # 拼接请求入参,多个请求&&隔开
        comm = self.cd_entry_path_comm
        for i in comm_list:
            comm = comm + "&&" + i
        log.get_log("serverClient",
                    "INFO",
                    "获取直连服务器配置host_name:{},port:{},user_name:{}\n拼接服务器命令:{}".format(
                        self.host_name,
                        self.port,
                        self.user_name,
                        comm
                    )
                    )
        try:
            log.get_log(
                "serverClient",
                "INFO",
                "----------[{}]任务开始处理---------".format(self.server_task_no)
            )
            # ssh免密连接并执行指定linux命令
            output = ssh(
                "{}@{}".format(self.user_name, self.host_name),
                "-p {}".format(self.port),
                comm
            )
            # 执行结果保存至指定服务器日志路径
            log.get_log(
                self.server_task_log_dir,
                "INFO",
                output
            )
            log.get_log(
                "serverClient",
                "INFO",
                "----------[{}]任务处理结束---------".format(self.server_task_no)
            )
        except Exception as e:
            log.get_log(
                "serverClient",
                "ERROR",
                "----------任务处理异常---------:{}".format(e)
            )

    def read_file(self) -> list:
        """
        读取执行服务器命令日志
        :return:
        """
        # 当前路径
        project_path = os.path.dirname(os.path.dirname(__file__))
        # 路径处理
        project_path = project_path.replace("public", "log/")
        # 拼接日志路径
        file_path_del = project_path + self.server_task_log_dir + str(datetime.datetime.now().strftime("/%Y_%m_%d.log"))
        with open(file_path_del, 'r+') as f:
            # 读取文件
            res = f.readlines()
            k_result = []
            # 提取ansi转义符
            for i in res:
                # 正则匹配
                rule = r'\x1b(.*?)m'
                v = re.findall(rule, i)
                if v:
                    # 获取匹配ansi转义符数量
                    ii = len(v)
                    # 循环读取ansi转义符
                    for nn in range(ii):
                        ansi_key = "\x1b{}m".format(v[nn])
                        # 添加至list
                        k_result.append(ansi_key)
            # 回显格式处理
            n = 0
            for i in res:
                i = i.replace("\\", "")
                i = i.replace("\n", "")
                i = i.replace(" INFO     | app.extensions.logger:get_log:70 ", "")
                # 去除ansi转义符
                if k_result:
                    for aa in k_result:
                        i = i.replace(aa, "")
                        res[n] = i
                else:
                    res[n] = i
                n += 1
            return res

    def read_log(
            self,
            server_log_name: str,
            read_comm: str = "cat",
            day_retrospective: int = 0
    ) -> any:
        """
        读取服务器日志
        :param server_log_name:服务器日志目录名
        :param read_comm: 读取linux命令
        :param day_retrospective: 向前追溯天数，默认0，查询当天
        :return:
        """
        now = datetime.datetime.now()
        # 日志路径预处理
        log_dir = (now - datetime.timedelta(days=day_retrospective)).strftime("%Y-%m/%Y-%m-%d.log")
        # 拼接日志路径
        log_dir = self.entry_path + "/log/" + server_log_name + "/" + log_dir
        # 拼接读取命令
        self.send(["{} {}".format(read_comm, log_dir)])
        # 读取执行结果
        res = self.read_file()
        return res


if __name__ == "__main__":
    c = Server_Sh(entry_name="module_equity_claim", dev="test")
    c.send(comm_list=["pwd"])
    rr = c.read_file()
    print(rr)
    # a = c.read_log(server_log_name="getPoolAmount", day_retrospective=3)
    # print(a)
