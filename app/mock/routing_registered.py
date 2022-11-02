from fastapi import FastAPI
from app.routers import test, server, redis
from app.routers import mock_db_data
from app.routers.policy.mock import drug, guarantee
from app.routers.policy import query, action


def register_router(app: FastAPI) -> None:
    """
    注册路由
    :param app:
    :return:
    """
    # 项目API
    # app.include_router(policy.router)
    app.include_router(mock_db_data.router)
    app.include_router(test.router)
    app.include_router(action.router)
    app.include_router(query.router)
    app.include_router(guarantee.router)
    app.include_router(drug.router)
    app.include_router(server.router)
    app.include_router(redis.router)
    # app.include_router(file_stream.router)
