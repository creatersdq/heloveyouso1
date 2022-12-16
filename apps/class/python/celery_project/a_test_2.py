import os

from classes.python.celery_project.tasks import add
from classes.python.celery_project.app import app

# print(app)
# os.system("job multi stopwait w1 -A app -l info")
# 关闭celery进程
# os.system("ps auxww|grep 'job'|grep -v grep|awk '{print $2}'|xargs kill -9")

"""
delay() 和 apply_async() 方法会返回一个 AsyncResult 实例，可以用于进行跟踪任务状况。
如果进行跟踪任务状态，需要设置一个结果后端，以便于存储。
"""
r = add.delay(1, 2)
"""
apply_async() 可以指定调用时执行的参数，例如运行的时间，使用的任务队列等：
add.apply_async((2, 2), queue='lopri', countdown=10)
"""
"""
如果任务执行引发异常，可以进行检查异常以及溯源，默认情况下 result.get() 会抛出异常：
如果不希望 Celery 抛出异常，可以通过设置 propagate 来进行禁用：
"""
# r.get(timeout=10)
# res.get(propagate=False)
"""
在这种情况下，他可以返回引发错误的实例，需要检查任务是否执行成功还是失败，可以通过在结果实例中使用对应的方法：
"""
#
# is_failed = r.failed()
# is_success = r.successful()
"""
  如何知道任务是否执行失败？可以通过查看任务的 state 进行查看
  一个任务只能有当前只能有一个状态，但他的执行过程可以为多个状态，一个典型的阶段是：PENDING -> STARTED -> SUCCESS
  启动状态是一种比较特殊的状态，仅在 task_track_started 启用设置或 @task(track_started=True)的情况下才会进行记录。 
  挂起状态实际上不是记录状态，而是未知任务ID的默认状态，可以从此实例中看到：
>>> from proj.job import app
>>> res = app.AsyncResult('this-id-does-not-exist')
>>> res.state
'PENDING'
 重试任务比较复杂，为了证明，一个任务会重试两次，任务的阶段为：
 PENDING -> STARTED -> RETRY -> STARTED -> RETRY -> STARTED -> SUCCESS
"""
# state = r.state
"""
也可以通过 id 属性进行获取任务的ID：
"""
# task_id = r.id

# job multi start w1 -A proj -l info
# job  multi restart w1 -A proj -l info
#
# # 异步关闭 立即返回
# job multi stop w1 -A proj -l info
# # 等待关闭操作完成
# job multi stopwait w1 -A proj -l info
