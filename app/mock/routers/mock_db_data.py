from fastapi import BackgroundTasks
from fastapi import APIRouter
from app.extensions import res_wrapper
from app.schems.mock_db_data import MockDbScript, SelectLogNum, SearchLog, SelectLog
from app.curd.db_log_num import get_log_num_status, search_limit, get_db_host, get_time
from app.public.mock_claim_per_records import mock_db_script, get_db_len
from app.extensions.pymysql_operation import get_log_data, hget_id
import os

router = APIRouter()


@router.post("/mock/unionDrug/udTest", tags=["同步数据"])
async def mock_db_data(item: MockDbScript, background_tasks: BackgroundTasks):
    pro_host_id = item.proHostId
    rc_host_id = item.rcHostId
    pro_table_schema = item.proTableSchema
    pro_table_name = item.proTableName
    rc_table_schema = item.rcTableSchema
    rc_table_name = item.rcTableName
    cycles = item.cycles
    num = item.num
    pr_db_len = get_db_len(pro_host_id, pro_table_schema, pro_table_name)
    log_num_status = get_log_num_status(pro_table_schema=pro_table_schema, pro_table_name=pro_table_name,
                                        rc_table_schema=rc_table_schema, rc_table_name=rc_table_name)
    if pr_db_len == "error":
        return res_wrapper.resp_200_error(message="error1", data="查询数据库库表错误，请核对")
    elif (log_num_status is None) and (int(pr_db_len) > int(cycles * num)):
        try:
            background_tasks.add_task(mock_db_script, pro_host_id, rc_host_id, pro_table_schema, pro_table_name,
                                      rc_table_schema, rc_table_name,
                                      cycles, num)
            return res_wrapper.resp_200(data="脚本正常执行")
        except Exception as e:
            return res_wrapper.resp_200_error(message="error1",
                                              data="执行异常:{}".format(e.args))
    elif log_num_status:
        return res_wrapper.resp_200_error(message="error1",
                                          data="当前数据库表已有脚本正在执行中，避免数据重复不要同时执行！！！")
    elif int(pr_db_len) < int(cycles * num):
        return res_wrapper.resp_200_error(message="error1",
                                          data="生产数据库数据总量:{}条, 少于同步的数据量：{}条。同步数据数量不能大于生产数据库数据量！！！".format(pr_db_len, (
                                                  cycles * num)))


@router.post("/mock/unionDrug/getProgressData", tags=["查询同步数据进度"])
def get_progress_data(item: SelectLogNum):
    log_num = item.logNum
    pro_host = item.proHost
    pro_table_schema = item.proTableSchema
    rc_table_name = item.rcTableName
    progress_data = hget_id(field=pro_host, dbname=pro_table_schema + "." + rc_table_name + "." + log_num)
    if progress_data == 0:
        return res_wrapper.resp_200(data="任务还没开始, 请先执行同步数据任务")
    else:
        return res_wrapper.resp_200(data=progress_data)


@router.post("/mock/unionDrug/getMockLog", tags=["查询同步数据log"])
async def get_mock_logo(item: SelectLog):
    log_num = item.logNum
    project_path = os.path.dirname(os.path.dirname(__file__))
    time, status = get_time(log_num)
    try:
        if status != "1":
            log_data = get_log_data(
                "{}/log/{}/{}.log".format(project_path, log_num, time))
            return res_wrapper.resp_200(data=log_data)
        else:
            return res_wrapper.resp_200(data="脚本正在执行，执行完再看日志")
    except Exception as e:
        return res_wrapper.resp_200(data="日志路径异常:{}".format(e.args))


@router.post("/mock/unionDrug/mockList", tags=["同步数据执行列表"])
async def get_mock_list(item: SearchLog):
    res_log_num = search_limit(item.dict())
    return res_wrapper.resp_200(data=res_log_num)


@router.get("/mock/unionDrug/getDB", tags=["获取数据库配置"])
async def get_db_name():
    try:
        res = get_db_host()
        return res_wrapper.resp_200(data=res)
    except Exception as e:
        return res_wrapper.resp_200_error(message="error1", data="接口请求失败:{}".format(e.args))
