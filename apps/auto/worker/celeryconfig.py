# # CELERY_TASK_SERIALIZER = 'json' # 配置序列化任务载荷的默认的序列化方式 有: pickle，JSON，YAML 和msgpack
# # CELERY_RESULT_SERIALIZER = 'json'
# # CELERY_ACCEPT_CONTENT = ["json"]
#
# BROKER_URL = 'redis://:uniondrug@123@192.168.3.133:6379/2' # 使用Redis作为消息代理
#
# CELERY_RESULT_BACKEND = 'redis://:uniondrug@123@192.168.3.133:6379/1' # 把任务结果存在了Redis
# # backend='redis://127.0.0.1:6379/5
# CELERY_RESULT_BROKER = 'redis://:uniondrug@123@392.168.3.133:6379/1'
# CELERY_TASK_SERIALIZER = 'msgpack' # 任务序列化和反序列化使用msgpack方案
#
# CELERY_RESULT_SERIALIZER = 'json' # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
#
# CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # 任务过期时间
#
# CELERY_ACCEPT_CONTENT = ['json', 'msgpack'] # 指定接受的内容类型