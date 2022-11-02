"""
读取处理测试数据
"""
import openpyxl
import sys
from apps.unify.tools.deal_path import CASE_DATA_DIR
from apps.extensions.logger import log


class ReadExcel(object):
    def __init__(self, file_name, sheet_name):
        self.file_name = file_name
        self.sheet_name = sheet_name

    def open_excel(self):
        # 获取表格
        self.wb = openpyxl.load_workbook(self.file_name)
        # 读取表单
        self.sh = self.wb[self.sheet_name]

    def read_excel(self):
        self.open_excel()
        # 读取数据 获取第一行数据，作为key
        list_01 = [x.value for x in list(self.sh.rows)[0]]

        # 读取数据 获取第二行以后的测试数据
        list_03 = []
        for i in list(self.sh.rows)[1:]:
            list_02 = [j.value for j in i]
            # 操作数据变成我们需要的格式[{},{}];  把key和value打包成一个字典
            dict_01 = dict(zip(list_01, list_02))
            list_03.append(dict_01)
        # 对于数据进行校验是否符合
        try:
            for i in list_03:

                if type(eval(i["relevance"])) != list:
                    # relevance中的数据不为列表
                    log.get_log(
                        "test_unify",
                        'INFO',
                        "处理数据--relevance数据校验失败;id为{}的relevance字段不为列表，此条数据为:{}，修改后重新提交".format(i['id'], i))
                    sys.exit("处理数据--relevance数据校验失败;id为{}的relevance字段不为列表，此条数据为:{}，修改后重新提交".format(i['id'], i))

                if type(eval(i["body"])) != dict:
                    # body中的数据不为字典
                    log.get_log(
                        "test_unify",
                        'INFO',
                        "处理数据--body数据校验失败;id为{}的body字段不为字典，此条数据为:{}，修改后重新提交".format(i['id'], i))
                    sys.exit("处理数据--body数据校验失败;id为{}的body字段不为字典，此条数据为:{}，修改后重新提交".format(i['id'], i))
                if i['method'].upper() not in ['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'PATCH', 'DELETE', 'TRACE',
                                               'CONNECT']:
                    # 请求方法书写有误
                    log.get_log(
                        "test_unify",
                        'INFO',
                        "处理数据--method数据校验失败;id为{}的请求方法书写有误，修改后重新提交".format(i['id']))
                    sys.exit("处理数据--method数据校验失败;id为{}的请求方法书写有误，此条数据为:{}，修改后重新提交".format(i['id'], i))

                if type(eval(i['assert_type'])) == list and type(eval(i['assert_field'])) == list and type(
                        eval(i['assert_value'])) == list:
                    pass

                else:
                    # 断言数据书写有误
                    log.get_log(
                        "test_unify",
                        'INFO',
                        "处理数据--assert_type/assert_field/assert_value不为列表，数据校验失败;id为{}的断言相关数据书写有误，修改后重新提交".format(
                            i['id']))
                    sys.exit(
                        "处理数据--assert_type/assert_field/assert_value不为列表，数据校验失败;id为{}的断言相关数据书写有误，此条数据为:{}，修改后重新提交".format(
                            i['id'], i))

                if len(eval(i['assert_type'])) != len(eval(i['assert_field'])) and eval(i['assert_value']) != len(
                        eval(i['assert_field'])):
                    log.get_log(
                        "test_unify",
                        'INFO',
                        "处理数据-assert_type/assert_field/assert_value数据长度不一致，数据校验失败;id为{}的断言数据assert_type、assert_field、assert_value字段长度不一致，修改后重新提交".format(
                            i['id']))
                    sys.exit(
                        "处理数据-assert_type/assert_field/assert_value数据长度不一致，数据校验失败;;id为{}的断言数据assert_type、assert_field、assert_value字段长度不一致，".format(
                            i['id'], i))

        except Exception as e:
            log.get_log(
                "test_unify",
                'INFO',
                "处理数据出现异常，异常信息为:{}".format(e))
            raise e

        list_04 = []
        for i in list_03:
            case_parent_code = i['case_parent_code']
            if case_parent_code not in list_04:
                list_04.append(case_parent_code)

        list_05 = []
        for i in list_04:
            list_06 = []
            for j in list_03:
                if j['case_parent_code'] == i:
                    list_06.append(j)
            list_05.append(list_06)
        return list_05


# if __name__ == '__main__':
#     import os
#
#     res = ReadExcel(os.path.join(CASE_DATA_DIR, "excel01.xlsx"), "Sheet1").read_excel()
#     print("返回的数据：", res)
