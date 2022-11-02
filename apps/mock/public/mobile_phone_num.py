# coding=UTF-8

import random
import string

# 运营商的号码前缀
prefix = [
    '130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
    '145', '147', '149', '150', '151', '152', '153', '155', '156', '157',
    '158', '159', '165', '171', '172', '173', '174', '175', '176', '177',
    '178', '180', '181', '182', '183', '184', '185', '186', '187', '188',
    '189', '191'
]


def builder():
    # 随机取一个手机号前缀
    pos = random.randint(0, len(prefix) - 1)
    # 随机生成后8位数字，string.digits是数字0到9，可以参考源码
    suffix = ''.join(random.sample(string.digits, 8))
    # 拼接返回11位手机号
    return prefix[pos] + suffix


if __name__ == "__main__":
    print(builder())
