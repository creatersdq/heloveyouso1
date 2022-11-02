import re
import paramiko
import os
import yaml

from time import sleep
from apps.extensions.logger import log


# 定义一个类，表示一台远端主机
class ServerClient:
    def __init__(self):
        self.yml_dir = ''
        self.entry_name = ''
        self.hostname = ''
        self.port = 22
        self.key = ''
        self.username = ''
        self.private_key = None
        self.timeout = 30  # 连接超时时间
        self.try_times = 3  # 失败重连次数

        # 初始化 transport和channel
        self.t = None
        self.c = None

    def get_config(self, yml_dir='ssh_config.yml', entry_name='module_equity_claim', dev='test') -> any:
        """
        获取服务器配置数据
        :param: yml_dir : 配置文件路径
        :param: entry_name : 服务器项目名
        :return:
        """
        self.yml_dir = yml_dir
        self.entry_name = entry_name + "_" + dev
        # 读取配置文件
        project_path = os.path.dirname(os.path.dirname(__file__))
        with open("{}/insurance_common/datas/{}".format(project_path, self.yml_dir), "r", encoding="utf-8") as f:
            file_data = f.read()
        data = yaml.safe_load(file_data)
        data = data[self.entry_name]

        # 获取配置参数
        self.hostname = data['SERVER_HOSTNAME']
        self.port = data['SERVER_PORT']
        self.key = data['PRIVATE_KEY']
        self.username = data['SERVER_USERNAME']
        self.private_key = paramiko.RSAKey.from_private_key_file(self.key)
        log.get_log("insurance_interconnection", "INFO",
                    "获取服务器配置>>服务器IP:{}>>端口号:{}>>本机密钥路径:{}>>登录用户名:{}".format(self.hostname, self.port, self.key,
                                                                            self.username))

    def connect(self) -> tuple:
        """
        连接服务器
        :param:
        :return:
        """
        while True:
            # 连接过程中可能会抛出异常，比如网络不通、链接超时
            try:
                self.t = paramiko.Transport((self.hostname, self.port))  # 建立一个加密的管道
                self.t.connect(username=self.username, pkey=self.private_key)
                # 打开一个通道
                self.c = self.t.open_session()
                self.c.settimeout(self.timeout)
                # 获取一个终端
                self.c.get_pty()
                # 激活器
                self.c.invoke_shell()
                # 如果没有抛出异常说明连接成功
                log.get_log("insurance_interconnection", "INFO", "连接服务器成功：{}".format(self.hostname))
                # 接收到的网络数据解码为str
                r = self.c.recv(65535).decode('utf-8')
                log.get_log("insurance_interconnection", "INFO", "{}".format(r))
                return self.t, self.c
            # 异常处理重试
            except Exception:
                if self.try_times != 0:
                    log.get_log("insurance_interconnection", "INFO", "连接{}失败，进行重试".format(self.hostname))
                    self.try_times -= 1
                else:
                    log.get_log("insurance_interconnection", "INFO", "重试3次失败，结束程序")
                    exit(1)

    def send(self, cmd: str) -> str:
        """
        执行服务器命令
        :param: cmd : linux命令
        :return:
        """
        cmd += '\r'
        # 通过命令执行符来判断命令是否执行完成
        p = re.compile(r']#')
        res = ''
        # 发送要执行的命令
        self.c.send(cmd)
        log.get_log("insurance_interconnection", "INFO", "执行服务器命令:{}".format(cmd))
        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        while True:
            sleep(0.5)
            ret = self.c.recv(65535)
            ret = ret.decode('utf-8')
            res += ret
            # 打印执行结果
            log.get_log("insurance_interconnection", "INFO", "打印执行结果".format(res))
            return res

    def close(self) -> any:
        """
        断开服务器连接
        :param:
        :return:
        """
        if self.c:
            self.c.close()
        if self.t:
            self.t.close()
        log.get_log("insurance_interconnection", "INFO", "断开服务器连接:{}".format(self.hostname))


if __name__ == '__main__':
    c = ServerClient()
    c.get_config('ssh_config.yml', 'module_equity_claim', 'test')
    p = c.connect()
    c.send('ls')
    c.close()
