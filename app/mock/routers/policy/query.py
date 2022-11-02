import json

from fastapi import APIRouter

from app.extensions import res_wrapper
from app.public.policy.query import QueryBase
from app.schems.policy.query import PolicyQuery, QUERYTYPE

router = APIRouter()


@router.post(
    "/policy/common/query",
    tags=["药品保-数据库数据查询"]
)
async def policy_query(items: PolicyQuery) -> res_wrapper:
    p = QueryBase(items.dev)
    res = ''
    # 投保任务关联表数据查询
    if items.type == QUERYTYPE.insureBatchQuery:
        try:
            res = json.loads(p.query_task_no_data(task_no=items.taskNo))
        except Exception as e:
            return res_wrapper.resp_200_error(message="投保任务关联数据查询失败:{}".format(e))
    # 投保结果关联表数据查询
    elif items.type == QUERYTYPE.insureResultQuery:
        try:
            res = json.loads(p.query_insured_result(task_no=items.taskNo))
        except Exception as e:
            return res_wrapper.resp_200_error(message="投保结果数据查询失败:{}".format(e))
    # mongoDB 数据查询
    elif items.type == QUERYTYPE.mongodbQuery:
        try:
            re = p.query_mongodb_data(
                collection=items.mongoDBCollection,
                key=items.mongoDBKey,
                value=items.mongoDBValue
            )
            res = json.loads(re)
        except Exception as e:
            return res_wrapper.resp_200_error(message="mongoDB数据查询失败:{}".format(e))
    else:
        return res_wrapper.resp_200_error(message="查询失败，数据类型异常，请检查")

    return res_wrapper.resp_200(data=res)
