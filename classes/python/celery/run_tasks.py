from tasks import add

result = add.delay(1, 2)
print('Is task ready: %s' % result.ready())  # False说明任务还没有执行完
run_result = result.get(timeout=1)
print('task result: %s' % run_result)
print('Is task ready: %s' % result.ready())

# cd celery
# celery -A tasks flower --broker=redis://uniondrug@123@192.168.3.133:6379/4
