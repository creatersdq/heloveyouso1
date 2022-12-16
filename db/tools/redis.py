from contextlib import contextmanager
from core.redispool import RedisPoolConnect


def redis_create(
        name: str,
        key: str = None,
        value: str = None,
        mapping: dict = None
) -> int:
    """

    :param name:
    :param key:
    :param value:
    :param mapping:
    :return:
    """
    with redis_conn() as conn:
        if mapping is None:
            res = conn.hset(
                name=name,
                key=key,
                value=value
            )

        if mapping is not None:
            res = conn.hset(
                name=name,
                mapping=mapping
            )
        return res


def redis_delete(
        name: str,
        key: str = None
) -> int:
    """

    :param name:
    :param key:
    :return:
    """
    with redis_conn() as conn:
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


def redis_update(
        name: str,
        key: str,
        value: str
) -> int:
    """

    :param name:
    :param key:
    :param value:
    :return:
    """
    with redis_conn() as conn:
        res = conn.hset(
            name=name,
            key=key,
            value=value
        )
        return res


def redis_query(
        name: str
) -> dict:
    """

    :param name:
    :return:
    """
    with redis_conn() as conn:
        res = {k.decode(): v.decode() for k, v in conn.hgetall(name).items()}
        return res


@contextmanager
def redis_conn():
    conn = None
    try:
        conn = RedisPoolConnect.make_redis_conn()
        yield conn
    except:
        if conn:
            conn.close()


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
