import redis
from apps.core.conf import setting


class RedisPoolConnectMate:
    def __init__(self):
        self.redis_pool = redis.ConnectionPool(host=setting()["REDIS"], password="uniondrug@123", port=6379,
                                               db=setting()["DB"])
        self.partners_redis_pool = redis.ConnectionPool(host="192.168.3.193", password="uniondrug@123", port=6379, db=0,
                                                        decode_responses=True)
        self.partners_redis_rc = redis.ConnectionPool(host="r-bp1ef3c20c012a54.redis.rds.aliyuncs.com",
                                                      password="UnionDrug@321", port=6379, db=0, decode_responses=True)

    def make_redis_conn(self):
        conn = redis.Redis(connection_pool=self.redis_pool)
        return conn

    def make_partner_redis_conn(self):
        conn = redis.Redis(connection_pool=self.partners_redis_pool)
        return conn

    def make_partner_redis_rc(self):
        conn = redis.Redis(connection_pool=self.partners_redis_rc)
        return conn


RedisPoolConnect = RedisPoolConnectMate()
