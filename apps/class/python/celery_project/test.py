import os
# 获取pid
import time

pid = os.getpid()
print(pid)
# 单个进程启动worker-异步任务


os.system("celery -A app worker -l info")
"""
其中-A表示创建的celery对象，-B表示启动定时，-l info日志输出等级是info
"""
# os.system("celery -A app worker -B -l info")

"""
可以通过设置运行职程（Worker）时指定职程（Worker）从某个队列中进行消费（celery worker -Q）：
"""
# os.system("celery -A app worker -Q hipri_0 -l info")
# time.sleep(10)
# print("等待10s结束")
# os.system("kill %s" % pid)
# print("kill 指定进程")
# os.system("celery multi start w1 -A app -l info")
# os.system("celery multi stopwait w1 -A app -l info")
# os.system("celery --broker=redis://:uniondrug@123@192.168.3.133:6379/6  flower ")
# os.system("celery -A app flower --address=127.0.0.1 --port=5555")
