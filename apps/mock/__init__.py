import traceback

import aiohttp
from fastapi import FastAPI, Request, Response, status, Depends
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, ValidationError
from apps.extensions import res_wrapper
from apps.extensions.logger import log
from apps.routers import policy, mock_db_data
from apps.routing_registered import register_router
import datetime
import time
from pyinstrument import Profiler


gl_session = None


def create_app() -> FastAPI:

    app = FastAPI(
        debug=False
    )

    @app.on_event("startup")
    def _startup():
        global gl_session
        gl_session = aiohttp.ClientSession()

    @app.middleware("http")
    async def response_cost_time(request: Request, call_next):
        """

        :param request:
        :param call_next:
        :return: 接口性能分析日志
        """
        profiler = Profiler()
        profiler.start()
        start_time = time.time()
        str_time = str(datetime.datetime.now())
        log.get_log("systemTime", "INFO",
                    "{str_time}->Request url:{req_url} to start".format(str_time=str_time, req_url=str(request.url)))
        response = await call_next(request)
        end_time = time.time()
        process_time = end_time - start_time
        log.get_log("systemTime", "INFO",
                    "{str_time}->Request url:{req_url} to end,the processing time is {process_time}".format(
                        str_time=str_time, req_url=str(request.url), process_time=process_time))
        profiler.stop()
        log.get_log("systemTime", "INFO", profiler.output_text())
        return response

    register_cors(app)
    register_router(app)
    register_exception(app)
    return app


def register_cors(app: FastAPI) -> None:
    """
    支持跨域
    :param app:
    :return:
    """

    # apps.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=["*"],
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )
    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8989",
        "http://localhost:8080",
        "http://front-opentest.uniondrug.net",
        "http://opentest-backend.uniondrug.net"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"], )


def register_exception(app: FastAPI) -> None:
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
        return res_wrapper.resp_500(message=traceback.format_exc())

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
        return res_wrapper.resp_5002(message=exc.errors())

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
        return res_wrapper.resp_4001(message=exc.errors())

    # @apps.exception_handler(TokenExpired)
    # async def user_not_found_exception_handler(request: Request, exc: TokenExpired):
    #     """
    #     token过期
    #     :param request:
    #     :param exc:
    #     :return:
    #     """
    #     log.get_log("info", "error",
    #                 f"token未知用户\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
    #
    #     return res_wrapper.resp_4003(message=exc.err_desc)
    #
    # @apps.exception_handler(TokenAuthError)
    # async def user_not_found_exception_handler(request: Request, exc: TokenAuthError):
    #     """
    #     token无效
    #     :param request:
    #     :param exc:
    #     :return:
    #     """
    #     log.get_log("info", "error",
    #                 f"用户认证异常\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
    #
    #     return res_wrapper.resp_4002(message=exc.err_desc)
