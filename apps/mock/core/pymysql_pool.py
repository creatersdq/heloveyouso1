import pymysql
from dbutils.pooled_db import PooledDB


def make_pymysql_conn(host, user, port, password, db_name):
    pool = PooledDB(pymysql, 5, host=host, user=user, port=port, password=password, db=db_name,
                               charset='utf8mb4', cursorclass=pymysql.cursors.SSDictCursor)
    conn = pool.connection()
    return conn