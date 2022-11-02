import functools
import json

from app.core.mock_db_common import DateBaseCommon
from app.curd.curd_redis import redis_query
from app.extensions.logger import log

# 获取redis配置
db_config = json.loads(redis_query(name='cn_ud_test_mock')["db_config"])

# 获取测试数据库配置
test_db_config = db_config["TEST_DB_CONFIG"]

# 获取rc数据库配置
rc_db_config = db_config['RC_DB_CONFIG']


def session_set(
        dev: str
) -> any:
    """
    初始化pymysql连接
    :param dev:
    :return:
    """
    try:
        # 药联测试库
        if dev == "yl_test":
            d = DateBaseCommon(
                test_db_config["DATABASE_NAME"],
                test_db_config["DATABASE_USERNAME"],
                test_db_config["DATABASE_PASSWORD"],
                test_db_config["DATABASE_HOST"],
                test_db_config["DATABASE_PORT"]
            )
            log.get_log(
                "policy_db_action",
                "INFO",
                "初始化-药联测试库-pymysql连接:{}".format(test_db_config)
            )
            conn = d.session_maker()
            return conn
        # 药联rc库
        elif dev == "yl_rc":
            d = DateBaseCommon(
                rc_db_config["DATABASE_NAME"],
                rc_db_config["DATABASE_USERNAME"],
                rc_db_config["DATABASE_PASSWORD"],
                rc_db_config["DATABASE_HOST"],
                rc_db_config["DATABASE_PORT"]
            )
            log.get_log(
                "policy_db_action",
                "INFO",
                "初始化-药联rc库-pymysql连接:{}".format(rc_db_config)
            )
            conn = d.session_maker()
            return conn
        # 财务测试库
        elif dev == "cw_test":
            d = DateBaseCommon(
                test_db_config["CW_DATABASE_NAME"],
                test_db_config["CW_DATABASE_USERNAME"],
                test_db_config["CW_DATABASE_PASSWORD"],
                test_db_config["CW_DATABASE_HOST"],
                test_db_config["CW_DATABASE_PORT"]
            )
            log.get_log(
                "policy_db_action",
                "INFO",
                "初始化-财务测试库-pymysql连接:{}".format(test_db_config)
            )
            conn = d.session_maker()
            return conn
        # 财务rc库
        elif dev == "cw_rc":
            d = DateBaseCommon(
                rc_db_config["CW_DATABASE_NAME"],
                rc_db_config["CW_DATABASE_USERNAME"],
                rc_db_config["CW_DATABASE_PASSWORD"],
                rc_db_config["CW_DATABASE_HOST"],
                rc_db_config["CW_DATABASE_PORT"]
            )
            log.get_log(
                "policy_db_action",
                "INFO",
                "初始化-财务rc库-pymysql连接:{}".format(rc_db_config)
            )
            conn = d.session_maker()
            return conn
    except Exception as e:
        log.get_log(
            "policy_db_action",
            "ERROR",
            "初始化-:{}-pymysql连接失败:{}".format(dev, e)
        )


# def db_conn(db_name):
#     """
#     数据库连接；
#     :param db_name:
#     :return:
#     """
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(dev: str, *args, **kw):
#             # 获取数据库连接
#             conn = session_set(db_name + dev)
#             print(conn)
#             print(type(conn))
#             # 执行sql函数
#             res = func(conn=conn, *args, **kw)
#             # 关闭数据库连接
#             if conn:
#                 conn.close()
#             return res
#         return wrapper
#     return decorator


if __name__ == '__main__':
    # print(test_db_config)
    # print(rc_db_config)
    # # print(test_db_config["CW_DATABASE_HOST"])
    # print(rc_db_config["DATABASE_NAME"])
    # print(rc_db_config["DATABASE_USERNAME"])
    # print(rc_db_config["DATABASE_PASSWORD"])
    # print(rc_db_config["DATABASE_HOST"])
    # print(rc_db_config["DATABASE_PORT"])
    c = session_set("yl_test")
    print(type(c))
