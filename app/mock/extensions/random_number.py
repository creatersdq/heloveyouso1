import time
import random


class StochasticNum(object):
    @staticmethod
    def water_no(a, b=None):
        now = time.strftime('%Y%m%d%H')
        if b:
            now = ""
        s = ''
        for i in range(3):
            letter_before = random.randint(65, 90)
            letter = chr(random.randint(97, 122))
            d = random.randint(0, 9)
            s1 = str(random.choice([d, letter, letter_before]))
            s = s + s1
        water_no = '{}'.format(a) + now + s[0:6]
        return water_no


if __name__ == '__main__':
    cc = StochasticNum.water_no("PN")
    print(cc)
