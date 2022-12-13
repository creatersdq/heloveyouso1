from celery import Celery

host_name = "192.168.3.133"
port = 6379
password = "uniondrug@123"
db_num = 4

backend_redis_url = 'redis://:%s@%s:%s/%s' % (password, host_name, port, db_num)
broker_redis_url = 'redis://:%s@%s:%s/%s' % (password, host_name, port, db_num)
# 第一个参数就是当前脚本的名称，
# backend 任务执行结果的存储地
# 址broker 任务队列的存储地址
app = Celery('tasks', backend=backend_redis_url, broker=broker_redis_url)

# redis://:password@hostname:port/db_number


@app.task
def add(x, y):
    return x + y
