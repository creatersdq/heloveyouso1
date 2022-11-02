from apps.core.pymysql_pool import make_pymysql_conn
from apps.extensions.pymysql_operation import get_id, select_data, insert_data
import os
import time
from tqdm import tqdm


def insert_claim_records_script(cycles: int, num: int):
    """
    claim_records 表批量插入数据
    :param cycles:  循环的次数
    :param num:  每次循环的数据量
    :return:
    """

    # 获取数据库表信息  生产环境
    host_select = 'rr-bp1u0dt3h26z4222i814.mysql.rds.aliyuncs.com'
    port_select = 3306
    user_select = 'uniondrug'
    pass_select = 'juyin@2017'
    dbname_select = 'cn_uniondrug_module_equity_claim_new'

    # 插入数据库表信息  rc环境
    host_insert = 'rm-bp1l9xe2xdx8oqf0x.mysql.rds.aliyuncs.com'
    port_insert = 3306
    user_insert = 'rctest_iud'
    pass_insert = 'tset@987#gurdnoinu'
    dbname_insert = 'cn_uniondrug_module_equity_claim_new'

    # 插入数据库表信息  测试环境
    # host_insert = 'udtest.uniondrug.com'
    # port_insert = 6033
    # user_insert = 'develop'
    # pass_insert = 'develop123'
    # dbname_insert = 'cn_uniondrug_module_equity_claim_new2'

    #######【！！！***查询和插入对应的数据库别弄反了***！！！】#######
    ### 连接查询数据库
    conn_select = make_pymysql_conn(host=host_select, port=port_select, user=user_select, password=pass_select, db_name=dbname_select)
    ### 连接插入数据库
    conn_insert = make_pymysql_conn(host=host_insert, port=port_insert, user=user_insert, password=pass_insert, db_name=dbname_insert)

    # 获取存放id标记的路径
    project_path = os.path.dirname(os.path.dirname(__file__))
    file_path = "{}/public/data/claim_records_id.txt".format(project_path)

    for i in tqdm(range(cycles)):
        # 获取id
        id = get_id("{}/public/data/claim_records_id.txt".format(project_path))
        # 查询数据的sql语句
        sql_select = "SELECT * FROM claim_records where id > {} ORDER BY id ASC limit {}".format(id, num)

        # 插入数据的sql语句
        sql_insert = "INSERT INTO `claim_records`(`batchId`, `subId`, `parentId`, `billNo`, `damageNo`, `equityNo`, " \
              "`policyNo`, `damageAmount`, `equityPremium`, `equityTotalPrice`, `userName`, `certificateNo`, `partnerName`, " \
              "`partnerCode`, `storeName`, `drugName`, `damageTime`, `confirmAmount`, `orderAmount`, `orderNo`, `memberNo`, " \
              "`gmtCreated`, `gmtUpdated`) " \
              "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        ## , `uniondrugPay`, `uniondrugPaid`, `uniondrugClaim`, `uniondrugClaimPaid`

        #查询数据
        data = select_data(conn=conn_select, sql=sql_select)

        # 列表推导式：把获取到数据转成列表，每个元素是一个字典
        list_data = [i for i in data]
        # 拿到最后一条数据到id最为标记
        last_id = list_data[-1]["id"]

        # 生成器：从数据列表中把每个字典中到value拿出来，生成（（1，1，1），（2，2，2）） 格式到元组，里面每个元素是一个元组，方便executemany（）批量插入
        list_tup = ((i["batchId"], i["subId"], i["parentId"], i["billNo"], i["damageNo"], i["equityNo"],
                     i["policyNo"], i["damageAmount"], i["equityPremium"], i["equityTotalPrice"], i["userName"],
                     i["certificateNo"], i["partnerName"],
                     i["partnerCode"], i["storeName"], i["drugName"], i["damageTime"], i["confirmAmount"], i["orderAmount"],
                     i["orderNo"], i["memberNo"],
                     i["gmtCreated"], i["gmtUpdated"]) for i in list_data)
        # , i["uniondrugPay"], i["uniondrugPaid"], i["uniondrugClaim"],i["uniondrugClaimPaid"]

        # 插入数据
        insert_data(conn=conn_insert, sql=sql_insert, data=list_tup, last_id=last_id, file_path=file_path)


if __name__ == '__main__':
    # a = time.time()
    # insert_script(5, 50000)
    # b = time.time()
    # time_c = b - a
    # print("花费时间： {} 秒".format(time_c))
    # for i in tqdm(range(1)):
    insert_claim_records_script(100, 500)