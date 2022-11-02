import pymongo
from apps.public.do_read_yaml import read_case_data
from apps.extensions.logger import log


class MongoDBClient(object):
    """
    mongoDB数据库连接
    """

    def __init__(self):
        self.data = read_case_data('cn_ud_test_mock/apps/core/mock_db_common.yml')
        self.test_mongodb_connect = self.data["TEST_DB_CONFIG"]["MONGODB_CONNECT"]
        self.rc_mongodb_connect = self.data["RC_DB_CONFIG"]["MONGODB_CONNECT"]
        self.conn = None
        log.get_log(
            "policy_db_action",
            "INFO",
            "获取mongoDB配置:{},:{},:{}".format(
                self.data,
                self.test_mongodb_connect,
                self.rc_mongodb_connect
            )
        )

    def get_mongo_conn(
            self,
            dev: str
    ) -> pymongo.mongo_client.MongoClient:
        """
        获取mongodb连接
        :param dev: 环境
        :return:
        """
        try:
            if dev == "test":
                self.conn = pymongo.MongoClient(
                    self.test_mongodb_connect,
                    connect=False,
                    maxPoolSize=2000
                )
                log.get_log(
                    "policy_db_action",
                    "INFO",
                    "获取:{}环境mongodb连接".format(dev)
                )
            elif dev == "rc":
                self.conn = pymongo.MongoClient(
                    self.rc_mongodb_connect,
                    connect=False,
                    maxPoolSize=2000
                )
                log.get_log(
                    "policy_db_action",
                    "INFO",
                    "获取:{}环境mongodb连接".format(dev)
                )
        except Exception as e:
            log.get_log(
                "policy_db_action",
                "ERROR",
                "获取:{}环境mongodb连接失败:{}".format(dev, e)
            )
        return self.conn


if __name__ == "__main__":
    c = MongoDBClient()
    a = c.get_mongo_conn("test")
    print(a)
    print(type(a))
