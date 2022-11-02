import os
import pytest
import allure

from apps.unify.case.deal_step import deal_test_step
from apps.unify.tools.deal_assert import DealAssert
from apps.unify.tools.tools import Unitst
from apps.unify.tools.deal_excel_case_datas import ReadExcel
from apps.unify.tools.deal_path import CASE_DATA_DIR

u = Unitst()


class TestUnify(object):
    get_datas = ReadExcel(os.path.join(CASE_DATA_DIR, "excel01.xlsx"), "Sheet1").read_excel()

    @pytest.mark.parametrize('args', get_datas)
    @allure.title("标题占位")
    def test_case_unify(self, args):
        t = 0
        for i in args:
            t = t + 1
            if t == 1:
                allure.dynamic.title("{}".format(i['case_title']))
            with allure.step(i['case_title']):
                result = deal_test_step(i)
                assert (DealAssert(i, result).deal_assert() is True)


if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', 'test_unify.py', '--clean-alluredir', '--alluredir=allure-results'])
    os.system(r"allure generate -c -o allure-report")
