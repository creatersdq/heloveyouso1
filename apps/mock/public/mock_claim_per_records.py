from apps.core.pymysql_pool import make_pymysql_conn
from apps.extensions.pymysql_operation import *
from tqdm import tqdm
from apps.extensions.logger import log
from apps.curd.db_log_num import add_num, update_num, get_db_name
from apps.extensions.random_number import StochasticNum


def get_db_len(pro_host_id: int, pro_table_schema: str, pro_table_name: str) -> any:
    """
    get_db_len 获取表的数据量
    :param pro_host_id 数据源实例id
    :param pro_table_schema:  生产的库名
    :param pro_table_name:  操作的表名
    :return: 对应库表的数据数量
    """
    # 【！！！***查询和插入对应的数据库别弄反了***！！！】
    # 连接查询数据库
    try:
        pro_host_data = get_db_name(pro_host_id)
        conn_select = make_pymysql_conn(host=pro_host_data["host"], port=pro_host_data["port"],
                                        user=pro_host_data["username"], password=pro_host_data["password"],
                                        db_name=pro_table_schema)
        db_data_sql = "select count(id) FROM `{}`.`{}`".format(pro_table_schema, pro_table_name)
        cursor = conn_select.cursor()
        cursor.execute(db_data_sql)
        db_len = cursor.fetchone()
        conn_select.close()
        return db_len["count(id)"]
    except Exception as e:
        return e


def mock_db_script(pro_host_id: int, rc_host_id: int, pro_table_schema: str, pro_table_name: str, rc_table_schema: str,
                   rc_table_name: str, cycles: int, num: int) -> any:
    """
    mock_db_script 表批量插入数据
    :param pro_host_id 数据源实例id
    :param rc_host_id 同步数据实例id
    :param pro_table_schema:  生产的库名
    :param rc_table_schema:  rc的库名
    :param pro_table_name:  获取数据的表名
    :param rc_table_name:  插入数据的表名
    :param cycles:  循环的次数
    :param num:  每次循环的数据量
    :return:
    """
    # 获取查询和插入的host配置
    pro_host_data = get_db_name(pro_host_id)
    rc_host_data = get_db_name(rc_host_id)
    # 生成标记号码：logNum_xxxxx
    log_num = StochasticNum().water_no("logNo_")
    # 新增一条执行中的数据
    add_num(pro_host=pro_host_data["host"], rc_host=rc_host_data["host"], pro_table_schema=pro_table_schema,
            rc_table_schema=rc_table_schema, num=num, cycles=cycles,
            pro_table_name=pro_table_name, rc_table_name=rc_table_name,
            log_num=log_num, status=1, pro_alias=pro_host_data['as_name'], rc_alias=rc_host_data['as_name'])
    # 【！！！***查询和插入对应的数据库别弄反了***！！！】
    # 连接查询数据库
    log.get_log(log_num, "INFO",
                "生产数据库名: {}，rc数据库名：{}, 插入的表名：{},循环的次数：{},每次循环执行的数据数量：{}".format(pro_table_schema, rc_table_schema,
                                                                                rc_table_name, cycles, num))
    try:
        conn_select = make_pymysql_conn(host=pro_host_data["host"], port=pro_host_data["port"],
                                        user=pro_host_data["username"], password=pro_host_data["password"],
                                        db_name=pro_table_schema)
        cursor_get = conn_select.cursor()
        # 连接插入数据库
        conn_insert = make_pymysql_conn(host=rc_host_data["host"], port=rc_host_data["port"],
                                        user=rc_host_data["username"], password=rc_host_data["password"],
                                        db_name=rc_table_schema)
        # 获得生产查询数据库的表字段的sql
        db_data_sql = "select COLUMN_NAME from information_schema.COLUMNS where table_schema='{}' and table_name = '{}'".format(
            pro_table_schema,
            pro_table_name)
        cursor_get.execute(db_data_sql)
        list_data = [i for i in cursor_get.fetchall() if i['COLUMN_NAME'] != "id"]
        # 拼接插入数据的sql语句
        db_field = tuple(i['COLUMN_NAME'] for i in list_data)
        db_field_last = ','.join(db_field)
        value = tuple('%s' for i in range(len(db_field)))
        value_sql = ",".join(value)
        sql_insert = "INSERT INTO `{}`.`{}`({})" \
                     "VALUES({})".format(rc_table_schema, rc_table_name, db_field_last, value_sql)
        log.get_log(log_num, "INFO", "查询表字段的sql：{}, 插入数据的sql:{}".format(db_data_sql, sql_insert))
        try:
            # 分次数循环获取批量数据插入数据
            for i in tqdm(range(cycles)):
                # 获取redis中存上次循环最后个数据id为这次循环的开始，没有则为0
                id = hget_id(field=pro_host_data["host"], dbname=pro_table_schema + "." + rc_table_name)
                # 查询数据的sql语句
                sql_select = "SELECT * FROM {}.{} where id > {} ORDER BY id ASC limit {}".format(pro_table_schema,
                                                                                                 pro_table_name, id,
                                                                                                 num)
                # 查询获取数据
                data = select_data(conn=conn_select, sql=sql_select, log_num=log_num)
                # 列表推导式：把获取到数据转成列表，每个元素是一个字典
                list_data1 = [i for i in data]
                # 拿到最后一条数据到id最为标记
                last_id = list_data1[-1]["id"]
                # 元组生成器：从数据列表中把每个字典中到value拿出来，生成（（1，1，1），（2，2，2）） 格式到元组，里面每个元素是一个元组，方便executemany（）批量插入
                list_tup = (tuple(j[i["COLUMN_NAME"]] for i in list_data) for j in list_data1)
                # 插入数据
                insert_data(conn=conn_insert, sql=sql_insert, host=pro_host_data["host"], data=list_tup,
                            table_schema=pro_table_schema, table_name=rc_table_name, log_num=log_num, last_id=last_id)
                log.get_log(log_num, "INFO",
                            "【数据插入成功】：本次循环获取数据开始的id：{},查询数据的sql：{}, 插入数据的最后id：{}".format(id, sql_select, last_id))
                # 更新存入执行进度
                hset_id(field=pro_host_data["host"], dbname=pro_table_schema + "." + rc_table_name + "." + log_num,
                        value=((i + 1) / cycles * 100))
            # 更新脚本执行状态为成功
            update_num(log_num=log_num, status=2)
        except Exception as e:
            log.get_log(log_num, "ERROR", "【执行失败的异常信息】：{}".format("获取数据活着插入数据错误{}".format(e.args)))
            # 更新存入执行进度
            hset_id(field=pro_host_data["host"], dbname=pro_table_schema + "." + rc_table_name + "." + log_num,
                    value="【执行异常】，请查看日志")
            # 更新脚本执行状态为执行异常
            update_num(log_num=log_num, status=3)
    except Exception as e:
        log.get_log(log_num, "ERROR", "【执行失败的异常信息】：{}".format("插入数据库连接失败"))
        # 更新存入执行进度
        hset_id(field=pro_host_data["host"], dbname=pro_table_schema + "." + rc_table_name + "." + log_num,
                value="【异常中断】，请查看日志:{}".format(e.args))
        # 更新脚本执行状态为执行异常
        update_num(log_num=log_num, status=3)
