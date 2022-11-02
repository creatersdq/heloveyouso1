import traceback

from fastapi import FastAPI, Request, Response, status, Depends
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, ValidationError
# from aioredis import create_redis_pool
from apps.extensions import new_response_wrapper
from apps.extensions.logger import log
from apps.routers import test1, case_run
from apps.extensions.depends_exc import TokenAuthError, TokenExpired
from apps.extensions.depends import token_dep
# from apps.core.date_base import SessionType


def create_app()-> FastAPI:
    app = FastAPI(
        debug=False
    )
    register_cors(app)
    register_router(app)
    register_exception(app)
    # register_db(apps)
    return app


def register_static_file(app: FastAPI)-> None:
    """
    静态文件交互开发模式使用
    生产使用 nginx 静态资源服务
    这里是开发是方便本地
    :param app:
    :return:
    """
    # from fastapi.staticfiles import StaticFiles
    # apps.mount("/static", StaticFiles(directory="static"), name="static")
    pass


def register_router(app: FastAPI)-> None:
    """
    注册路由
    这里暂时把两个API服务写到一起，后面在拆分
    :param app:
    :return:
    """
    # 项目API
    # apps.include_router(test1.router)
    app.include_router(case_run.router)



def register_cors(app: FastAPI)-> None:
    """
    支持跨域
    :param app:
    :return:
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_exception(app: FastAPI)-> None:
    # # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        全局所有异常
        :param request:
        :param exc:
        :return:
        """
        log.get_log('result', 'error',
                    f"token未知用户\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return new_response_wrapper.resp_500(message=traceback.format_exc())

    @app.exception_handler(ValidationError)
    async def inner_validation_exception_handler(request: Request, exc: ValidationError):
        """
        内部参数验证异常
        :param request:
        :param exc:
        :return:
        """
        log.get_log("info", "error",
                    f"内部参数验证错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return new_response_wrapper.resp_5002(message=exc.errors())

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        请求参数验证异常
        :param p:
        :param exc:
        :return:
        """
        log.get_log("info", "error",
                    f"请求参数格式错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return new_response_wrapper.resp_4001(message=exc.errors())

    @app.exception_handler(TokenExpired)
    async def user_not_found_exception_handler(request: Request, exc: TokenExpired):
        """
        token过期
        :param request:
        :param exc:
        :return:
        """
        log.get_log("info", "error",
                    f"token未知用户\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

        return new_response_wrapper.resp_4003(message=exc.err_desc)

    @app.exception_handler(TokenAuthError)
    async def user_not_found_exception_handler(request: Request, exc: TokenAuthError):
        """
        token无效
        :param request:
        :param exc:
        :return:
        """
        log.get_log("info", "error",
                    f"用户认证异常\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

        return new_response_wrapper.resp_4002(message=exc.err_desc)


# def register_redis(apps: FastAPI) -> None:
#     """
#     把redis挂载到app对象上面
#     :param apps:
#     :return:
#     """
#
#     @apps.on_event('startup')
#     async def startup_event():
#         """
#         获取链接
#         :return:
#         """
#         # apps.state.redis = await create_redis_pool(settings.REDIS_URL)
#         logging.log("event", "error", "redis以启动")
#         apps.state.redis = await create_redis_pool("redis://127.0.0.1:6379/1")
#
#     @apps.on_event('shutdown')
#     async def shutdown_event():
#         """
#         关闭
#         :return:
#         """
#         apps.state.redis.close()
#         await apps.state.redis.wait_closed()
#         logging.log("event", "error", "事件结束")

# def register_db(apps: FastAPI) -> None:
#     @apps.on_event('startup')
#     def startup_event():
#         apps.state.db = SessionType()
#         log.get_log("event", "error", "db已启动")
