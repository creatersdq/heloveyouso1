import random


def random_no(
        quantity:
        int
) -> str:
    """
    随机整数字符串
    :param quantity: 位数
    :return:
    """
    a = ''
    for i in range(quantity):
        a = a + str(random.randint(0, 9))
    return a


if __name__ == '__main__':
    print(random_no(32))
