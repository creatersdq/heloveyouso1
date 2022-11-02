#
# from __future__ import absolute_import
# from celery import Celery, platforms
#
# celeryapp = Celery('celery_app'
# #
# #     broker='redis://127.0.0.1:6379/4',
# #     backend='redis://127.0.0.1:6379/5'
# )
# celeryapp.config_from_object('worker.celeryconfig') # 调用 config_from_object() 来让 Celery 实例加载配置模块
# celeryapp.autodiscover_tasks(['worker.tasks'])
# # platforms.C_FORCE_ROOT = True
# # broker="redis://:uniondrug@123@192.168.3.133:6379/2",
# # backend="redis://:uniondrug@123@192.168.3.133:6379/3",
