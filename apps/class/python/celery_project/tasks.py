import time
from job import group
from classes.python.celery_project.app import app


@app.task
def add(*arg):
    r = 0
    for i in arg:
        r += i
    return r


@app.task
def x_sum(x, y):
    return x + y


@app.task()
def add_t():
    pass


@app.task()
def add_task(cal_list):
    """
    group任务构建
    """
    ll = group(add.s(i) for i in cal_list)
    r = ll().get()
    return r
