import json

from fastapi import APIRouter

from apps.extensions import res_wrapper
from apps.schems.redis import RedisCurd
from apps.curd.curd_redis import redis_create, redis_query, redis_update, redis_delete

router = APIRouter()


@router.post(
    "/common/redis/create",
    tags=["redis-新增"]
)
async def policy_actions(items: RedisCurd) -> res_wrapper:
    res = redis_create(
        name=items.name,
        key=items.key,
        value=items.value
    )
    return res_wrapper.resp_200(data=res)


@router.post(
    "/common/redis/delete",
    tags=["redis-删除"]
)
async def policy_actions(items: RedisCurd) -> res_wrapper:
    res = redis_delete(
        name=items.name,
        key=items.key
    )
    return res_wrapper.resp_200(data=res)


@router.post(
    "/common/redis/update",
    tags=["redis-修改"]
)
async def policy_actions(items: RedisCurd) -> res_wrapper:
    res = redis_update(
        name=items.name,
        key=items.key,
        value=items.value
    )
    return res_wrapper.resp_200(data=res)


@router.post(
    "/common/redis/query",
    tags=["redis-查询"]
)
async def policy_actions(items: RedisCurd) -> res_wrapper:
    res = redis_query(name=items.name)
    # res1 = json.dumps(res, indent=4, ensure_ascii=False)
    return res_wrapper.resp_200(data=res)
