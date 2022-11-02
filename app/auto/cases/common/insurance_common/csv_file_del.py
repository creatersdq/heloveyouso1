import csv
import json
import os
import random
import requests

from apps.cases.common.insurance_common.datetime_cal import today_day
from apps.cases.common.insurance_common.do_path import BASE_DIR


class CsvFileDel(object):

    def __init__(self):
        self.premium = 100
        self.amount = 100120
        self.equityNo = ''
        self.water_no = ''  # 投保标UUID
        self.name = ''
        self.insured_id_no = ''
        self.startDate = '2020-05-19'
        self.endDate = '长期'
        self.address = '南京市玄武区银城东苑73号302室'
        self.date = ''

    def uuid_set(self):
        """
        自定义流水号
        """
        # 抬头
        l1 = 'PN'
        # 日期年月格式处理
        self.date = str(today_day).replace('-', '')
        l2 = ''
        # 生成22位随机数字
        l3 = [random.randint(1, 9) for x in range(1, 22)]
        # 遍历list
        for i in l3:
            l2 += str(i)
        # 拼接字符串
        water_no = l1 + self.date + l2
        self.water_no = water_no

    def insure_csv(self, equity_no_quantity):
        """
        自定义投保csv文件
        :param:equity_no_quantit投保标人数
        """
        # 列头
        headers = ('UUID', '投保码', '保额', '保费', '姓名', '身份证号', '身份证起期', '身份证止期', '地址')
        data_list = []
        # 拼接文件名: uuid+.csv
        file_name = "csv_files/" + self.water_no + ".csv"
        # csv文件编码格式
        encoding = 'utf-8'
        with open(file_name, 'w', encoding=encoding, newline='') as f:
            write = csv.writer(f)  # 创建writer对象
            write.writerow(headers)
            start_id = 5136746
            count = 1
            i = 0
            while count <= equity_no_quantity:
                self.equityNo = get_object(start_id).equityNo
                self.name = get_object(start_id).insuredName
                self.insured_id_no = get_object(start_id).insuredIdNo
                output = (
                    self.water_no, self.equityNo, self.amount, self.premium, self.name, self.insured_id_no,
                    self.startDate,
                    self.endDate, self.address)
                data_list.append(1)
                data_list[i] = output
                i += 1
                count += 1
                start_id -= 1
            # 写内容，writerrow 一次只写入一行
            for data in data_list:
                write.writerow(data)

    def file_upload(self):
        """
        上传测试服务器,生成线上地址
        """
        pass

    def policy_insure_csv(self):
        """
        自定义保司投保文件
        """
        pass

    def upload_csv_file(self):
        """
        上传服务器，生成线上文件地址
        """
        data_dir = os.path.join(BASE_DIR, 'cases/common/insurance_common/csv_files/')
        file_route = data_dir + self.water_no + ".csv"
        print(data_dir)
        url = 'http://opentest-backend.uniondrug.net/api/claim/upload'
        kw = {"files": "'/Users/uniondrug/Desktop/PN463706666794039818606796050706.csv'"}
        response = requests.post(url, data=kw, type="file")
        print(response.json())


if __name__ == '__main__':
    c = CsvFileDel()
    c.uuid_set()
    # c.insure_csv(1)
    c.upload_csv_file()
