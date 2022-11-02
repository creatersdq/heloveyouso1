import random
import time
import datetime


def create_store_id():
    """生成一个六位数字的字符串"""
    random_store_id = random.randint(100000, 999999)
    return str(random_store_id)


def create_order_no():
    """生成订单的20为的订单号orderNo"""
    time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    time2 = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
    str_time = datetime.datetime.strftime(time2, '%Y%m%d%H%M%S')
    random_order_no = str_time + str(random.randint(100000, 999999))
    return random_order_no


if __name__ == '__main__':
    res = create_order_no()
    # res = create_store_id()
    print(res, type(res))
