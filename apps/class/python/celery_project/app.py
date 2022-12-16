import os
import sys
from datetime import timedelta
from job import Celery

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)
# sys.path.append(BASE_DIR)


app = Celery('celery_project', include=["classes.python.celery_project.tasks"])
app.config_from_object("classes.python.celery_project.celeryconfig")
print(app.conf)

# 路由
# app.conf.update(
#     # task_routes={
#     #     'proj.tasks.add': {'queue': 'hipri_0'},
#     #     'proj.tasks.x_sum': {'queue': 'hipri_1'}
#     # },
#     # CELERYBEAT_SCHEDULE={
#     #     'add': {
#     #         'task': 'classes.python.celery_project.tasks.add',
#     #         'schedule': timedelta(seconds=10),
#     #         'args': (16, 16)
#     #     }
#     # },
#     # timezone='Asia/Shanghai'
# )

# 定时任务调度


if __name__ == "__main__":
    app.start()
