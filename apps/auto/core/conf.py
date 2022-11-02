"""
    ***获取yaml文件数据***
    # yaml键值对：即python中字典
    usr: my
    psw: 123455
    类型：<class 'str'>
    ***转化yaml数据为字典或列表***
    {'usr': 'my', 'psw': 123455}
    类型：<class 'dict'>
"""

import yaml
from functools import lru_cache
import os
from typing import Optional
from pathlib import Path


class GlobalConfig:
    # def __init__(self):
    # conf_path=Path.cwd()
    conf_path = os.path.dirname(__file__)
    with open("{}/config.yml".format(conf_path), 'r', encoding="utf-8") as f:
        file_data = f.read()
    config_file = yaml.safe_load(file_data)
    env_status = config_file['ENV_STATE']


class DevConfig(GlobalConfig):
    def __call__(self):
        return GlobalConfig.config_file['DEVCONFIG']


class ProdConfig(GlobalConfig):
    def __call__(self):
        return GlobalConfig.config_file['PROCONFIG']


class TestConfig(GlobalConfig):
    def __call__(self):
        return GlobalConfig.config_file['TESTCONFIG']


class FactoryConfig:
    def __init__(self, env_status: Optional[str]):
        self.env_status = env_status

    def __call__(self):
        if self.env_status == "dev":
            return DevConfig()()
        elif self.env_status == "pro":
            return ProdConfig()()
        elif self.env_status == "test":
            return TestConfig()()


@lru_cache()
def setting():
    return FactoryConfig(GlobalConfig.env_status)()


setting()
