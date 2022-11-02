import json
import os
import paramiko
import datetime

from time import sleep
from app.extensions.random_number import StochasticNum
from app.curd.curd_redis import redis_query
from app.extensions.logger import log


class ServerClient(object):

    def __init__(
            self,
            dev: str,
            entry_name: str
    ):
        """

        :param dev: 环境，test,rc
        :param entry_name: 目标主机项目名
        """
        # 堡垒机
        self.proxy_config = json.loads(redis_query(name='cn_ud_test_mock')["server_config"])["PROXY"]
        self.proxy_hostname = self.proxy_config["PROXY_HOSTNAME"]
        self.proxy_port = self.proxy_config["PROXY_PORT"]
        self.proxy_username = self.proxy_config["PROXY_USERNAME"]
        self.proxy_key = self.proxy_config["PROXY_PRIVATE_KEY"]
        self.proxy_private_key = paramiko.RSAKey.from_private_key_file(self.proxy_key)
        self.proxy_password = self.proxy_config["PROXY_PASSWORD"]

        # 目标主机
        self.target_config = json.loads(redis_query(name='cn_ud_test_mock')["server_config"])[entry_name + "_" + dev]
        self.target_hostname = self.target_config["SERVER_HOSTNAME"]
        self.target_port = self.target_config["SERVER_PORT"]
        self.target_path = "cd " + self.target_config["PATH"]

        self.timeout = 10  # 连接超时时间
        self.try_times = 3  # 失败重连次数
        self.ssh = None

        # 服务器日志路径
        self.server_log_dir = ''
        self.sever_log_path = ''

        # 堡垒机连接
        self.proxy_client = None
        self.invoke = None

        self.target_connect_comm = self.target_config["ORDER"]
        self.comm_list = [self.target_path]

    def send(
            self,
            cmd: list
    ) -> str:
        """
        执行服务器命令
        :param: cmd : linux命令
        :return:
        """
        # 服务器日志路径预处理
        # 年-月
        today = str(datetime.datetime.now().strftime("%Y-%m")) + "/"
        # 年-月-日
        today_time = str(datetime.datetime.now().strftime("%Y-%m-%d")) + "/"
        # 日志文件名
        log_dir_name = "/" + str(datetime.datetime.now().strftime("%Y_%m_%d")) + ".log"
        # 自定义任务编号
        log_num = StochasticNum().water_no("serverTask")
        # 日志路径
        self.server_log_dir = "serverTask/" + today + today_time + log_num
        # 日志文件名
        self.sever_log_path = self.server_log_dir + log_dir_name

        self.proxy_client = paramiko.SSHClient()
        self.proxy_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 连接堡垒机
        log.get_log("serverClient",
                    "INFO",
                    "连接堡垒机\nhostname:{}\nport:{}\nusername:{}\npkey:{}\n".format(
                        self.proxy_hostname,
                        self.proxy_port,
                        self.proxy_username,
                        self.proxy_key
                    )
                    )
        self.proxy_client.connect(
            hostname=self.proxy_hostname,
            port=self.proxy_port,
            username=self.proxy_username,
            timeout=self.timeout,
            pkey=self.proxy_private_key
        )
        self.invoke = self.proxy_client.invoke_shell()
        for i in cmd:
            self.comm_list.append(i)
        # 连接目标主机
        self.invoke.send(self.target_connect_comm.encode())
        log.get_log("serverClient",
                    "INFO",
                    "连接服务器：{},执行服务器命令：{}".format(
                        self.target_hostname,
                        self.target_connect_comm
                    )
                    )
        # 等待时间
        sleep(2)
        login_res = self.invoke.recv(65535).decode()
        log.get_log(
            "serverClient",
            "INFO",
            login_res
        )
        res = ''
        # 循环执行服务器命令
        try:
            # 发送要执行的命令
            for execute_comm in self.comm_list:
                execute_comm += '\r'
                self.invoke.send(execute_comm)
                # 回显很长的命令可能执行较久，通过循环分批次取回回显
                while True:
                    sleep(0.5)
                    ret = self.invoke.recv(65535)
                    ret = ret.decode()
                    res += ret
                    is_complete = res.find(']$')
                    # 通过是否存在"]$"字符判断命令是否执行完成
                    if is_complete != -1:
                        # 格式处理
                        res = res.replace("\x1b[0m", "")
                        res = res.replace("\x1b[32;1m", "")
                        log.get_log(
                            self.server_log_dir,
                            "INFO",
                            "{}".format(res)
                        )
                        # 恢复初始值
                        res = ''
                        break
                    else:
                        res = res
            return log_num
        except Exception as e:
            log.get_log(
                self.server_log_dir,
                "ERROR",
                "执行服务器命令失败:{}".format(e)
            )

    def close(self) -> any:
        """
        断开服务器连接
        :param:
        :return:
        """
        if self.invoke:
            self.invoke.close()
        if self.proxy_client:
            self.proxy_client.close()
        log.get_log(
            "serverClient",
            "INFO",
            "断开服务器连接"
        )

    def read_file(
            self,
            server_log_path: str
    ) -> list:
        """
        读取log文件
        :param server_log_path:文件路径
        :return:
        """
        project_path = os.path.dirname(os.path.dirname(__file__))
        project_path = project_path.replace(
            "public/",
            "log/"
        )
        file_path_del = project_path + server_log_path
        with open(file_path_del, 'r+') as f:
            # 读取数据
            res = f.readlines()
            # 格式处理
            n = 0
            for i in res:
                i = i.replace("\n", "")
                i = i.replace(" app.extensions.logger:get_log:70 - ", "")
                res[n] = i
                n += 1
            return res


if __name__ == "__main__":
    s = ServerClient(entry_name="module_equity_claim", dev="rc")
    c = s.send(["pwd"])
    # d = s.read_file("server_command_execute" + "/2022-09" + "/2022-09-21/" + c + "/2022_09_21.log")
    # print(d)
    # print(len(d))
    # print(c)
    s.close()
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect('47.110.156.126', port=60022, username='sun.daqing', password='qing0221qing', timeout=10)
    # invoke = ssh.invoke_shell()
    # # invoke.send("jj\n")
    # invoke.send(":")
    # invoke.send("192.168.3.191:36022\n")
    # sleep(2)  # 等待命令执行完毕
    # # invoke.send("\n")
    # # sleep(2)  # 等待命令执行完毕
    # # invoke.send("\n")
    # # sleep(2)
    # invoke.send("pwd\n")
    # sleep(5)  # 等待命令执行完毕
    # a = invoke.recv(99999).decode()
    # print(a)
    # ssh.close()

# import datetime
# import json
# import os
#
# from time import sleep
# from app.curd.curd_redis import redis_query
# from app.extensions.logger import log
#
# # 定义一个类，表示一台远端主机
# from app.extensions.random_number import StochasticNum


# class ServerClientOs(object):
#     def __init__(self):
# self.entry_name = entry_name
# self.server_config = json.loads(redis_query(name='cn_ud_test_mock')["server_config"])[entry_name + "_" + dev]
# self.hostname = self.server_config["SERVER_HOSTNAME"]
# self.port = str(self.server_config["SERVER_PORT"])
# self.entry_path = "cd " + self.server_config["PATH"]
# self.result = []

# def connect(self):
#     ssh_comm = "ssh -p {} {}".format(self.port, self.hostname)
#     cd_comm = self.entry_path
#     output1 = os.popen(ssh_comm)
#     res = output1.read()
#     log.get_log("server_client", "info", res)
#     output2 = os.popen(cd_comm)
#     res = output2.read()
#     log.get_log("server_client", "info", res)

# def send(self, comm):
#     output = os.popen(comm)
#     res = output.read()
#     print(res)
#     log.get_log("server_client", "info", res)

# def exit(self):
#     output = os.popen("exit")
#     res = output.read()
#     log.get_log("server_client", "info", res)


# if __name__ == '__main__':
#     # s = ServerClientOs(dev="test", entry_name="module_equity_claim")
#     s = ServerClientOs()
#     # s.connect()
#     # s.exit()
#     s.send("ssh -p 60022 sun.daqing@47.110.156.126 -tt")
#     s.send("jjjjjj\n")
#     s.send("who")
#     # s.send("ssh  -p 36022 192.168.3.191")
#     # s.send("exit")
#     print(s.result)
