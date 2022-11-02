# quality.autotest

## 依赖

- 依赖->文件

* pip3 freeze > requirements.txt

- 全局依赖更新

* pip3 install -r requirements.txt

## 异步任务

- 队列启动

* celery -A task worker -l info

- 开启队列管理监听

* flower -A task --port=5555

- 守护进程模式开启队列

* sudo celery multi start w1 -A task -l info --logfile=./celerylog.log

## supervisor

- 启动

* supervisord -c supervisord.conf

- 关闭

* supervisorctl -c supervisord.conf shutdown

- 重启

* supervisorctl -c supervisord.conf reload

```python
print("hello world")
```
