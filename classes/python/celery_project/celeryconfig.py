BROKER_URL = 'redis://:uniondrug@123@192.168.3.133:6379/6'  # 配置消息队列，默认使用 RabbitMQ
# BROKER_URL = 'amqp://dongwm:123456@localhost:5672/web_develop' # 使用RabbitMQ作为消息代理，默认地址
# 'amqp://guest:**@127.0.0.1:5672/'
CELERY_BROKER_URL = 'redis://:uniondrug@123@192.168.3.133:6379/6'
# 把任务结果存在了Redis 区分生成的key，使用不同的库，使用 keys * 查看  把任务结果存在了Redis
COSMOSDBSQL_MAX_RETRY_WAIT_TIME = 5
CELERY_RESULT_BACKEND = 'redis://:uniondrug@123@192.168.3.133:6379/6'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
CELERY_TASK_RESULT_EXPIRES = 60 * 24 * 24  # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显
CELERY_ACCEPT_CONTENT = ["json"]  # 指定任务接受的内容类型
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_ENABLE_UTC = True
"""
下面这个就是限制tasks模块下的add函数，每秒钟只能执行10次
或者限制所有的任务的刷新频率
CELERY_ANNOTATIONS = {'*':{'rate_limit':'10/s'}}

也可以设置如果任务执行失败后调用的函数
def my_on_failure(self,exc,task_id,args,kwargs,einfo):
    print('task failed')

CELERY_ANNOTATIONS = {'*':{'on_failure':my_on_failure}}

"""
# CELERY_ANNOTATIONS = {'task.add': {'rate_limit': '10/s'}}
"""
并发的worker数量，也是命令行-c指定的数目
事实上并不是worker数量越多越好，保证任务不堆积，加上一些新增任务的预留就可以了
"""
CELERYD_CONCURRENCY = 20
CELERYD_PREFETCH_MULTIPLIER = 4




