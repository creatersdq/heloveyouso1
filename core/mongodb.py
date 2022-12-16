from contextlib import contextmanager

import pymongo

from pymongo.mongo_client import MongoClient
from extension.do_read_yaml import read_case_data
from extension.logger import log


class MongoDBConn(object):
    """
    mongoDB数据库连接
    """

    # 记录第一个被创建对象的引用
    instance = None
    # 记录是否执行过初始化动作
    init_flag = False

    # 重写__new__方法
    def __new__(cls, *args, **kwargs):
        # 判断类属性是否是空对象
        if MongoDBConn.instance is None:
            # 调用父类的方法，为第一个对象分配空间
            MongoDBConn.instance = object.__new__(cls)
        # 返回类属性保存的对象引用
        return MongoDBConn.instance

    def __init__(self):
        # 判断当前对象是否执行过初始化动作
        if not MongoDBConn.init_flag:
            self.data = read_case_data('cn_ud_test_mock/app/core/mock_db_common.yml')
            self.test_conn_info = self.data["TEST_DB_CONFIG"]["MONGODB_CONNECT"]
            self.rc_conn_info = self.data["RC_DB_CONFIG"]["MONGODB_CONNECT"]
            self.conn_info = None
            self.conn = None
            # init_flag标记为true，下次创建对象时不再执行初始化动作
            MongoDBConn.init_flag = True

    def get_mongo_conn(
            self,
            dev: str
    ) -> MongoClient:
        """
        获取mongodb连接
        :param dev: 环境
        :return:
        """
        # 根据环境获取mongoDB配置
        if dev == "test":
            self.conn_info = self.test_conn_info
        elif dev == "rc":
            self.conn_info = self.rc_conn_info
        # 连接mongoDB数据库
        if self.conn_info:
            self.conn = pymongo.MongoClient(
                self.conn_info,
                connect=False,
                maxPoolSize=2000)
        return self.conn

    @contextmanager
    def mongo_db_conn(self, dev) -> any:
        try:
            self.conn = self.get_mongo_conn(dev)
            log.get_log(
                "mongoDB",
                "INFO",
                "获取mongoDB连接:{}".format(
                    self.conn_info
                )
            )
            yield self.conn
        except Exception as e:
            log.get_log(
                "mongoDB",
                "ERROR",
                "获取:{}环境mongodb连接失败:{}".format(dev, e)
            )
        finally:
            if self.conn:
                self.conn.close()


if __name__ == "__main__":
    c = MongoDBConn()
    a = c.get_mongo_conn("test")
    print(a)
    print(type(a))
