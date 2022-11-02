"""

统一响应状态码

"""
from typing import Union

from fastapi import status
from fastapi.responses import JSONResponse, Response


def resp_200(data=None) -> Response:
    if data is None:
        data = []
    elif type(data) is list:
        # 根据字典第一个KEY 进行升序
        try:
            data = sorted(data, key=lambda elem: elem['{}'.format(list(elem.keys())[0])])
        except:
            pass
    else:
        pass
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'errno': 0,
            'dataType': "OBJECT",
            'error': "",
            'data': data
        }
    )


def resp_500(message: str = "Internal Server Error") -> Response:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'errno': 500,
            'dataType': "ERROR",
            'error': message,
            'data': []
        }
    )


# 请求参数格式错误
def resp_4001(
        message: Union[list, dict, str] = "Request Validation Error") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'errno': 4001,
            'dataType': "ERROR",
            'error': "Request Validation Error",
            'data': message
        }
    )


# token认证失败
def resp_4002(message: str = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'errno': 4002,
            'dataType': "ERROR",
            'error': message,
            'data': []
        }
    )


# 用户token过期
def resp_4003(message: str = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'errno': 4003,
            'dataType': "ERROR",
            'error': message,
            'data': []
        }
    )


# 内部验证数据错误
def resp_5002(message="Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'errno': 5002,
            'dataType': "ERROR",
            'error': "Request Validation Error",
            'data': message
        }
    )


def resp_200_error(message, data=None) -> Response:
    if data is None:
        data = []
    else:
        data = data
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'errno': "001",
            'dataType': "ERROR",
            'error': "{}".format(message),
            'data': data
        }
    )
