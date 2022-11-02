from requests import request

from apps.extensions.logger import log


def common_request(method, url, header, params):
    """统一请求接口"""
    try:
        res = request(method=method, url=url, headers=header, json=params).json()
        return res
    except Exception as e:
        log.get_log(
            "test_unify",
            'INFO',
            "******request请求报错******入参数据分别为：method:{}; url:{}; headers:{}; params:{}; 报错信息为:{}".format(method, url,
                                                                                                       header,
                                                                                                       params, e))
        return False
