import redis
from apps.core.conf import setting


class RedisConnect:
    def __init__(self):
        self.redis_pool = redis.ConnectionPool(host=setting()["REDIS"], password="uniondrug@123", port=6379, db=setting()["DB"])

    def make_redis_conn(self):
        conn = redis.Redis(connection_pool=self.redis_pool)
        return conn


RedisPoolConnect = RedisConnect()
