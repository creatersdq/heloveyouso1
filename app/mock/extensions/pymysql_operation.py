import pymysql
from app.extensions.logger import log
from app.core.redispool import RedisPoolConnect

coon = RedisPoolConnect.make_redis_conn()


# 写入成功的最后一个id
def update_id(filepath_id, content):
    with open(filepath_id, 'w+') as f:
        f.writelines(content)


# 获取上次写入的id
def get_id(filepath_id):
    with open(filepath_id, 'r+') as f:
        data = f.readlines()
        return int(data[-1])


# 获取执行表的日志
def get_log_data(filepath):
    try:
        with open(filepath, 'r+') as f:
            data = f.readlines()
            return data
    except Exception as e:
        return "获取日志失败:{}".format(e.args)


# 写入redis中hash值
def hset_id(field, dbname, value):
    res = coon.hset(name=field, key=dbname, value=value)
    return res


# 获取redis中hash值
def hget_id(field, dbname):
    res = coon.hget(name=field, key=dbname)
    if res is None:
        return 0
    else:
        res.decode()
        return res.decode()


# 获取数据
def select_data(conn, sql, log_num) -> any:
    """
    id: 所查对象表中数据的id
    range: 一次查询的数量
    conn: 连接数据库
    生成器方式获取数据
    """
    cursor = conn.cursor()

    try:
        with cursor as db_cursor:
            db_cursor.execute(sql)
            result = db_cursor.fetchone()
            while result is not None:
                yield result
                result = db_cursor.fetchone()
        log.get_log(log_num, "INFO",
                    "【数据获取成功】：获取数据的sql：{}".format(sql))
    except Exception as e:
        conn.close()
        log.get_log(log_num, "ERROR",
                    "【数据获取失败】：{}".format(e))


# 插入数据
def insert_data(conn, data, sql, host, table_schema, table_name, log_num, last_id=None):
    """
    元组生成器转化成导入需要的数据格式
    :param conn:  连接数据库
    :param data:  转成Generator格式批量插入
    :param sql:     插入sql
    :param host:  执行的表名称
    :param table_schema: 库
    :param table_name: 表
    :param log_num: 执行编号
    :param last_id:  标记插入成功的最后一个id，不需要的可以不传
    :return:
    """
    cursor = conn.cursor()

    # 批量插入成功则提交事物保存，记录log
    try:
        cursor.executemany(sql, data)
        conn.commit()
        hset_id(field=host, dbname=table_schema + "." + table_name, value=last_id)
        log.get_log(log_num, "INFO",
                    "【数据插入成功】：插入数据的最后id：{}".format(last_id))
    # 批量插入失败则回滚事务，记录log
    except pymysql.Error as e:
        conn.rollback()
        conn.close()
        log.get_log(log_num, "ERROR",
                    "【数据插入失败】：{}".format(e))
