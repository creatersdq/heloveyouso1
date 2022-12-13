# tasks.py
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def send_email(to, message):
    # 模拟发送邮件
    print("send email to {to} with message: {message}".format(to=to, message=message))


# main.py
send_email.delay('zhangsan@xxx.com', '哥们，你中大奖了')  # 通知张三
