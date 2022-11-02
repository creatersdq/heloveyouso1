import requests

from apps.cases.common.insurance_common.do_read_yaml import read_case_data
from parse import parse, search


class Base(object):
    def __init__(self, conf='server_data.yaml'):
        self.yml_dir = ''
        self.case_data = ''
        self.conf = conf
        self.case_data = read_case_data(self.conf)

    def get_path(self, path: str) -> str:
        """
        获取脚本执行路径
        :param: path : 路径key
        :return: 脚本执行路径
        """
        r = self.case_data[path]
        p = r['PATH']
        return p

    def get_command(self, plan: str) -> str:
        """
        获取获取脚本命令
        :param: plan : 脚本key
        :return: 脚本命令
        """
        base = 'php' + ' ' + 'console' + ' ' + 'lockPlan'
        d = self.case_data[plan]
        comm = base + d['para1'] + d['para2'] + d['para3']
        return comm

    def get_log(self, start: str, stop: str, ass: str) -> str:
        """
        截取str
        :param: start : 开始字符
        :param: stop : 结束字符
        :param: ass : str
        :return: 截取内容
        """
        res = search(start + '{}' + stop, ass)
        return res[0]


if __name__ == '__main__':
    c = Base()
    print(c.get_command('ZIJIN_0_0'))
    print(c.get_path('SERVER_PATH_RC'))
    print(c.get_log("1", "2", "132"))

