def consumer():
    r = ''
    while True:
        print('[CONSUMER] 挂起')
        n = yield r
        print('[CONSUMER] 恢复--并接受到数据%s' % n)
        result = '200 OK'


def produce(func):
    print('[PRODUCER] 准备启动协程')
    next(func)
    sendData = 0
    while sendData < 2:
        sendData = sendData + 1
        print('[PRODUCER] 发送数据 %s' % sendData)
        result = coroutine.send(sendData)
        print('[PRODUCER] 处理结果: %s' % result)
    coroutine.close()


coroutine = consumer()
produce(coroutine)
