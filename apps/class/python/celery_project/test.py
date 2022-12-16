import os
# 获取pid
import time

pid = os.getpid()
print(pid)
# 单个进程启动worker-异步任务


os.system("job -A app worker -l info")
"""
其中-A表示创建的celery对象，-B表示启动定时，-l info日志输出等级是info
"""
# os.system("job -A app worker -B -l info")

"""
可以通过设置运行职程（Worker）时指定职程（Worker）从某个队列中进行消费（job worker -Q）：
"""
# os.system("job -A app worker -Q hipri_0 -l info")
# time.sleep(10)
# print("等待10s结束")
# os.system("kill %s" % pid)
# print("kill 指定进程")
# os.system("job multi start w1 -A app -l info")
# os.system("job multi stopwait w1 -A app -l info")
# os.system("job --broker=redis://:uniondrug@123@192.168.3.133:6379/6  flower ")
# os.system("job -A app flower --address=127.0.0.1 --port=5555")
