import time
from celery import group

from classes.python.celery_project.tasks import *

t_0 = add.s(1, 2)
t_1 = add.s(2, 3)
t_group = group(t_0, t_1)
t_list = [t_0, t_1]
for i in t_list:
    i.delay()
# r = t_group.delay()
# print(r)
# c = r.get()
# print(c)

# r = build(group_obj)

# print(r)
# data_1 = add.s(1, 2)
# data_2 = add.s(2, 2)
# r = group(data_1, data_2)().get()
# r = data_1.delay()
# r(1).get(timeout=10)
# state = r.state
# result = r.result
