import csv
from apps.extensions.random_number import StochasticNum
from apps.public.mock_chinese_name import RandomChineseName
from apps.public.identity import IdNumber
import random
from apps.public.mobile_phone_num import builder

random_num = StochasticNum()


# 报销型太平csv投保文件
class CsvClass:
    def __init__(self, uuid: str, premium):
        gt = int((premium - premium % 2400) / 2400)
        self.rows = [

        ]
        self.uuid = uuid
        self.headers = ["药联出单请求uuid", "投保码", "姓名", "身份证", "身份证起期", "身份证止期", "地址", "手机号", "赔付金额"]
        for i in range(2000):
            policy_num = StochasticNum.water_no("607468", 1)
            chinese_name = RandomChineseName.random_name_str()
            id_card_num = IdNumber.generate_id(random.randint(0, 1))
            id_card_start = "2008-09-27"
            id_card_end = "2028-09-27"
            address = "安徽省淮北市相山区春秋巷3栋103室"
            iphone_num = builder()
            claim_amount = 2488
            self.rows.append(
                [self.uuid, policy_num, chinese_name, id_card_num, id_card_start, id_card_end, address, iphone_num,
                 claim_amount])

    def taiping_bx(self):
        with open("./taiping_policy/{}.csv".format(self.uuid), 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(self.headers)
            f_csv.writerows(self.rows)
        # with open(csv_file, 'w') as f:
        #     f_csv = csv.writer(f)
        #     f_csv.writerow(self.headers)
        #     f_csv.writerows(self.rows)


if __name__ == '__main__':
    tt = CsvClass(random_num.water_no("PN"), 70000)
    tt.taiping_bx()
