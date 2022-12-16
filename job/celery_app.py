import os
import sys


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from celery import Celery
from celery.utils.log import get_task_logger

app = Celery('job', include=["app.job.task"])
# 定义配置文件路径
app.config_from_object("app.job.celery_config")

# 创建 logger，以显示日志信息
celery_log = get_task_logger(__name__)

# 配置
app.conf.update(
    task_routes={
        'app.job.task.post': {'queue': 'post_task_job_app'},
        'app.job.task.add': {'queue': 'add_task_job_app'}
    },
    # 定时任务
    # CELERYBEAT_SCHEDULE={
    #     'add': {
    #         'task': 'app.job.task.add',
    #         'schedule': timedelta(seconds=10),
    #         'args': (16, 16)
    #     }
    # }
)

# if __name__ == "__main__":
#     app.start()
