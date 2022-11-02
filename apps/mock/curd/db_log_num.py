from apps.core.data_base import session_maker
from apps.models.log_num import LogNum, DbNameAll
from sqlalchemy.sql import func
from datetime import datetime


def get_log_num_status(pro_table_schema, pro_table_name, rc_table_schema, rc_table_name):
    """
    get_num 查询当前对应数据库表为执行中的
    :param pro_table_schema:
    :param pro_table_name:
    :param rc_table_schema
    :param rc_table_name
    :return:logNum
    """
    with session_maker() as db:
        res = db.query(func.max(LogNum.id), LogNum.status).filter(LogNum.proTableSchema == pro_table_schema,
                                                                  LogNum.proTableName == pro_table_name,
                                                                  LogNum.rcTableSchema == rc_table_schema,
                                                                  LogNum.rcTableName == rc_table_name,
                                                                  LogNum.status == 1).scalar()

    return res


def get_data(log_num_id) -> list:
    """
    get_data 根据id查询数据
    :param log_num_id:
    :return:logNum
    """
    with session_maker() as db:
        res = db.query(LogNum.proHost, LogNum.logNum, LogNum.status).filter(LogNum.id == log_num_id).one()
    return res


def get_host_log_num(log_num_id):
    """
    get_num 查询操作的库的logNum
    :param log_num_id:
    :return:logNum
    """
    with session_maker() as db:
        res = db.query(LogNum.proHost, LogNum.logNum, LogNum.status).filter(LogNum.id == log_num_id).one()
    return res


def get_time(log_num):
    """
    get_time 查询更新时间和状态
    :param log_num:
    :return
    """
    with session_maker() as db:
        res = db.query(LogNum.gmtUpdated, LogNum.status).filter(LogNum.logNum == log_num).one()
        time = res[0].strftime('%Y_%m_%d')
        status = res[1]
    return time, status


def add_num(pro_host, pro_alias, rc_alias, rc_host, pro_table_schema, rc_table_schema, pro_table_name, rc_table_name,
            log_num, status, num, cycles):
    with session_maker() as db:
        db.add(LogNum(proHost=pro_host, proAlias=pro_alias, rcHost=rc_host, rcAlias=rc_alias,
                      proTableSchema=pro_table_schema, rcTableSchema=rc_table_schema,
                      proTableName=pro_table_name,
                      rcTableName=rc_table_name,
                      logNum=log_num, status=status, num=num, cycles=cycles))


def update_num(log_num, status):
    """
    :param log_num
    :param status
    :return:
    """
    with session_maker() as db:
        db.query(LogNum).filter(LogNum.logNum == log_num).update({"status": status})


def search_log_data(item: dict) -> dict:
    """
    logNum查询
    param:item：dict，直接传入接口入参
    return:log_dict
    """
    db_sql = 'SELECT * FROM log_num WHERE'
    count_db_sql = 'SELECT count(id) FROM log_num WHERE'

    page_size = item["pageSize"]
    page_num = item["pageNum"]
    del item['pageSize']
    del item['pageNum']

    for i in [k for k, v in item.items() if v is None]:
        del item[i]
    db_filer = []
    if item:
        if "id" in item:
            db_filer.append(" and id = {}".format(item["id"]))
        if "proHost" in item:
            db_filer.append(" and proHost = '{}'".format(item["proHost"]))
        if "rcHost" in item:
            db_filer.append(" and rcHost = '{}'".format(item["rcHost"]))
        if "proTableSchema" in item:
            db_filer.append(" and proTableSchema = '{}'".format(item["proTableSchema"]))
        if "proTableName" in item:
            db_filer.append(" and proTableName = '{}'".format(item["proTableName"]))
        if "rcTableSchema" in item:
            db_filer.append(" and rcTableSchema = '{}'".format(item["rcTableSchema"]))
        if "rcTableName" in item:
            db_filer.append(" and rcTableName = '{}'".format(item["rcTableName"]))
        if "logNum" in item:
            db_filer.append(" and logNum = '{}'".format(item["logNum"]))
        if "status" in item:
            db_filer.append(" and status = '{}'".format(item["status"]))

    else:
        db_sql = db_sql.replace("WHERE", "")
        count_db_sql = count_db_sql.replace("WHERE", "")

    for i in range(len(db_filer)):
        if i == 0:
            db_sql += db_filer[0].replace("and", "")
            count_db_sql += db_filer[0].replace("and", "")
        else:
            db_sql += db_filer[i]
            count_db_sql += db_filer[i]
    db_sql = db_sql + " order by id desc limit {} offset {}".format(page_size, (page_num - 1) * page_size)
    print(db_sql)
    with session_maker() as db:
        res = list(db.execute(db_sql))
        total = list(db.execute(count_db_sql))
        log_num_data_list = list(
            map(lambda x: {"id": x[0], "proHost": x[1], "rcHost": x[2], "proTableSchema": x[3], "proTableName": x[4],
                           "rcTableSchema": x[5], "rcTableName": x[6], "logNum": x[7], "status": x[8]}, res))
    return {"logNumList": log_num_data_list, "total": total[0][0]}


def search_limit(search_dict):
    page_size = search_dict["pageSize"]
    page_num = search_dict["pageNum"]
    del search_dict['pageSize']
    del search_dict['pageNum']
    for i in [k for k, v in search_dict.items() if v is None]:
        del search_dict[i]
    # 获取页码后，删除，且删除value is None的key
    with session_maker() as db:
        res = db.query(LogNum.proHost, LogNum.rcHost, LogNum.proTableSchema, LogNum.proTableName, LogNum.rcTableSchema,
                       LogNum.rcTableName, LogNum.logNum, LogNum.status, LogNum.id, LogNum.proAlias,
                       LogNum.rcAlias, LogNum.num, LogNum.cycles).order_by(LogNum.id.desc()).limit(
            page_size).offset(
            (page_num - 1) * page_size).all()
        total = db.query(func.count(LogNum.id)).scalar()
        res_list = [
            {"proHost": x[0], "rcHost": x[1], "proTableSchema": x[2], "proTableName": x[3], "rcTableSchema": x[4],
             "rcTableName": x[5], "logNum": x[6], "status": x[7], "id": x[8], "rcAlias": x[10], "proAlias": x[9],
             "num": x[11], "cycles": x[12]} for x
            in res]
        return {"resList": res_list, "total": total}


def search_lognum_data() -> list:
    """
    查询log_num 所有数据
    :return:
    """
    with session_maker() as db:
        res = db.query(LogNum.id, LogNum.proHost, LogNum.rcHost, LogNum.proTableSchema, LogNum.proTableName,
                       LogNum.rcTableSchema, LogNum.rcTableName, LogNum.logNum, LogNum.status,
                       LogNum.gmtUpdated).order_by(-LogNum.id).all()
        res_log_num_data = []
        for i in res:
            data_dict = dict()
            data_dict["id"] = i[0]
            data_dict["proHost"] = i[1]
            data_dict["rcHost"] = i[2]
            data_dict["proTableSchema"] = i[3]
            data_dict["proTableName"] = i[4]
            data_dict["rcTableSchema"] = i[5]
            data_dict["rcTableName"] = i[6]
            data_dict["logNum"] = i[7]
            data_dict["status"] = i[8]
            data_dict["gmtUpdated"] = i[9].strftime('%Y_%m_%d')
            res_log_num_data.append(data_dict)
    return res_log_num_data


def get_db_host():
    """
    :return:
    """
    with session_maker() as db:
        res = db.query(DbNameAll.id, DbNameAll.host, DbNameAll.asName, DbNameAll.envType, DbNameAll.status).filter(
            DbNameAll.status == 1).all()
        list_data = []
        for i in res:
            data_dict = dict()
            data_dict["id"] = i[0]
            data_dict["host"] = i[1]
            data_dict["as_name"] = i[2]
            data_dict["env"] = i[3]
            data_dict["status"] = i[4]
            list_data.append(data_dict)
    return list_data


def get_db_name(db_id):
    """
    :param db_id:
    :return:
    """
    with session_maker() as db:
        res = db.query(DbNameAll.id, DbNameAll.host, DbNameAll.port, DbNameAll.userName, DbNameAll.passWord,
                       DbNameAll.asName).filter(
            DbNameAll.id == db_id).one()
    return {"id": res[0], "host": res[1], "port": res[2], "username": res[3], "password": res[4], "as_name": res[5]}
