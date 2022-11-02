import pymysql

'''通过ssh连接mysql-生产连锁数据库'''
class ProChainConn:
    def _conn(self):
        self.conn = pymysql.connect(
            host='rr-bp1q4dt7n859530zw.mysql.rds.aliyuncs.com',  # 固定写法
            port=3306,
            user="deploy",  # 数据库账号
            passwd="deploy2018",  # 数据库密码
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    def exec_sql(self,sql):
        try:
            self._conn() # # 调用私有方法，让连接再次开启
            self.cursor.execute(sql)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            print(e)
        #发生错误时回滚s
            # self.conn.rollback
        finally:
            self.conn.close()
            # self.server.close()

# print(ProChainConn().exec_sql('select * from partners_manage.partners limit 1'))
