import json
import time

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager
from db.redis import redis_query
from extension.logger import log


# = event.listens_for(before_cursor_execute)
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(
        db_conn,
        cursor,
        statement,
        parameters,
        context,
        executemany
):
    """
    监听执行sql，并添加日志
    """
    # sql开始执行时间
    context._query_start_time = time.time()
    # sql语句
    log.get_log("db", "INFO", "Start Query:\n%s" % statement)
    # 入参
    log.get_log("db", "INFO", "Parameters:\n%r" % (parameters,))


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(
        db_conn,
        cursor,
        statement,
        parameters,
        context,
        executemany
):
    """
    监听执行sql完成后，并添加日志
    """
    # 计算执行时间
    total = time.time() - context._query_start_time
    # 执行完成
    log.get_log("db", "INFO", "Query Complete!")
    # 执行时间
    log.get_log("db", "INFO", "Total Time: %.02fms" % (total * 1000))


class DBConn(object):
    """
    创建数据库连接
    """

    # 记录第一个被创建对象的引用
    instance = None

    # 重写__new__方法
    def __new__(cls, *args, **kwargs):
        # 如果类属性为空对象
        if DBConn.instance is None:
            # 分配内存空间
            DBConn.instance = object.__new__(cls)
        # 返回类属性对象变量
        return DBConn.instance

    def __init__(self, env):
        self.db_config = json.loads(redis_query(name='cn_ud_test_mock')["db_config"])  # 数据库配置
        self.test_db_config = self.db_config["TEST_DB_CONFIG"]  # 测试数据库配置
        self.rc_db_config = self.db_config['RC_DB_CONFIG']  # rc数据库配置
        self.env = env
        self.s = None

    def get_conn(self):
        # 根据环境获取数据库配置信息
        if self.env == "yl_test":
            name = self.test_db_config["DATABASE_NAME"]
            user_name = self.test_db_config["DATABASE_USERNAME"]
            password = self.test_db_config["DATABASE_PASSWORD"]
            host = self.test_db_config["DATABASE_HOST"]
            port = self.test_db_config["DATABASE_PORT"]
        elif self.env == "yl_rc":
            name = self.rc_db_config["DATABASE_NAME"]
            user_name = self.rc_db_config["DATABASE_USERNAME"]
            password = self.rc_db_config["DATABASE_PASSWORD"]
            host = self.rc_db_config["DATABASE_HOST"]
            port = self.rc_db_config["DATABASE_PORT"]
        elif self.env == "cw_test":
            name = self.test_db_config["CW_DATABASE_NAME"]
            user_name = self.test_db_config["CW_DATABASE_USERNAME"]
            password = self.test_db_config["CW_DATABASE_PASSWORD"]
            host = self.test_db_config["CW_DATABASE_HOST"]
            port = self.test_db_config["CW_DATABASE_PORT"]
        elif self.env == "cw_rc":
            name = self.rc_db_config["CW_DATABASE_NAME"]
            user_name = self.rc_db_config["CW_DATABASE_USERNAME"]
            password = self.rc_db_config["CW_DATABASE_PASSWORD"]
            host = self.rc_db_config["CW_DATABASE_HOST"]
            port = self.rc_db_config["CW_DATABASE_PORT"]
        else:
            raise "env must in  [yl_test,yl_rc,cw_test,cw_rc]"

        # 连接信息
        conn_info = "mysql+pymysql://{}:{}@{}:{}/{}".format(
            user_name,
            password,
            host,
            port,
            name
        )
        engine = create_engine(
            conn_info,
            pool_recycle=3600,
            pool_pre_ping=True,
            echo=False
        )
        base = declarative_base()
        session_type = scoped_session(
            sessionmaker(
                bind=engine,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False
            )
        )
        self.s = session_type()
        log.get_log("db",
                    "INFO",
                    "获取数据库连接\n环境：%s\n%s\n%s\n%s\n%s\n%s\n" % (self.env, host, port, name, user_name, password))

    @contextmanager
    def session_maker(self):
        try:
            self.get_conn()
            yield self.s
            self.s.commit()
        except:
            self.s.rollback()
            raise
        finally:
            self.s.close()
