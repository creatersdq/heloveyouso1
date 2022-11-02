from __future__ import absolute_import
from datetime import timedelta
from celery import Celery

celery_app = Celery(
    'worker',
    backend='redis://:uniondrug@123@192.168.3.133:6379/6',  # 存储结果
    broker='redis://:uniondrug@123@192.168.3.133:6379/6'  # 消息中间件
)

# 路由任务,新增队列auto-queue 负责处理自动化脚本运行
celery_app.conf.task_routes = {
    "worker.celery_worker.async_run_scp": "auto-queue",
    "worker.celery_worker.add": "auto-queue",
    "worker.celery_worker.add1": "auto-queue",
}
# 定时任务
celery_app.conf.update(
    task_track_started=False,
    beat_schedule={
        'ptask': {
            'worker': 'worker.celery_worker.beat_task',
            'schedule': timedelta(seconds=5)
        }
    },
    timezone='Asia/Shanghai'
)
