import json

from redis import Redis

from app.core.redispool import RedisPoolConnect
from app.public.do_read_yaml import read_case_data


def redis(func):
    def wrapper(*args, **kw):
        # 创建redis连接
        redis_conn = RedisPoolConnect.make_redis_conn()
        res = func(conn=redis_conn, *args, **kw)
        # 关闭redis连接
        if redis_conn:
            redis_conn.close()
        return res

    return wrapper


@redis
def redis_create(
        conn: Redis,
        name: str,
        key: str = None,
        value: str = None,
        mapping: dict = None
) -> int:
    """

    :param conn:
    :param name:
    :param key:
    :param value:
    :param mapping:
    :return:
    """
    if mapping is None:
        res = conn.hset(
            name=name,
            key=key,
            value=value
        )
        return res
    if mapping is not None:
        res = conn.hset(
            name=name,
            mapping=mapping
        )
        return res


@redis
def redis_delete(
        conn: Redis,
        name: str,
        key: str = None
) -> int:
    """

    :param conn:
    :param name:
    :param key:
    :return:
    """

    if key is None:
        # 删除键
        res = conn.delete(name)
        return res
    if key is not None:
        # 删除指定key
        res = conn.hdel(
            name,
            key
        )
        return res


@redis
def redis_update(
        conn: Redis,
        name: str,
        key: str,
        value: str
) -> int:
    """

    :param conn:
    :param name:
    :param key:
    :param value:
    :return:
    """
    res = conn.hset(
        name=name,
        key=key,
        value=value
    )
    return res


@redis
def redis_query(
        conn: Redis,
        name: str
) -> dict:
    """

    :param conn:
    :param name:
    :return:
    """
    res = {k.decode(): v.decode() for k, v in conn.hgetall(name).items()}
    return res


if __name__ == "__main__":
    # 1
    # a = redis_delete(name='mock_config')
    # 1
    # a = redis_create(name='cn_ud_test_mock', key='mock_config', value=config_data)
    # 0
    # a = redis_update(name='cn_ud_test_mock', key='mock_config', value=config_data)
    # a = redis_query(name='cn_ud_test_mock')
    # config1 = json.dumps(read_case_data('cn_ud_test_mock/app/core/mock_data.yml'))
    # config2 = json.dumps(read_case_data('cn_ud_test_mock/app/core/ssh_config.yml'))
    # config3 = json.dumps(read_case_data('cn_ud_test_mock/app/core/mock_db_common.yml'))
    # print(config1)
    # a = redis_create(name='cn_ud_test_mock', key='mock_config', value=config1)
    # b = redis_create(name='cn_ud_test_mock', key='server_config', value=config2)
    # d = redis_create(name='cn_ud_test_mock', key='db_config', value=config3)
    aa = redis_query(name='cn_ud_test_mock')
    print(aa)
    print(type(aa))
    a = redis_delete(name="cn_ud_test_mock", key="1")
