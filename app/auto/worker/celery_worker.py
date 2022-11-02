import time
from time import sleep
import inspect
import sys
import os

# sys.path.append("/Users/living/PythonPrj/quality.autotest/apps")
# sys.path.append("/Users/living/PythonPrj/quality.autotest")
# sys.path.append("/Users/living/PythonPrj/quality.autotest/apps/worker")
cc = os.getcwd()
bb = os.path.abspath(os.path.dirname(os.getcwd()))
dd = os.path.abspath(os.path.dirname(bb))
sys.path.append(cc)
sys.path.append(dd)
sys.path.append(bb)

from celery import current_task, Task
from celery.utils.log import get_task_logger
from apps.worker.celery_app import celery_app


class MyTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        print(f'task done: {retval}')
        return super(MyTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f'task fail, reason:{exc}')
        time.sleep(3)
        return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    for i in range(1, 11):
        sleep(1)
        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': i * 10})
    return f"test task return {word}"


# 执行测试脚本
@celery_app.task(bind=True,name="worker.celery_worker.async_run_scp")
def async_run_scp( self,prj: str, prj_name: str, plan_no: str):
    from apps.new_run import run_case
    run_case(prj, prj_name, plan_no)


logger = get_task_logger(__name__)


# 绑定任务为实例
@celery_app.task(bind=True, name='worker.celery_worker.add1')
def add1(self, x, y):
    logger.info(self.request.__dict__)
    print(6666)
    return x + y


# 定时/周期任务
@celery_app.task(bind=True)
def beat_task(self):
    return (f'beat task done: {self.request.id}')


# 链式任务 return  2n + 1
@celery_app.task(acks_late=True)
def arg1(x):
    # sleep(10)
    print(123, 23, 123)
    return x


@celery_app.task(acks_late=True)
def arg2(y):
    return 2 * y


@celery_app.task(acks_late=True)
def chain_task(z):
    return z + 1


def run_chain_task():
    '''
    2 * 3 + 1 = 7
    '''
    ch = arg1.s(3) | arg2.s() | chain_task.s()
    ch()
