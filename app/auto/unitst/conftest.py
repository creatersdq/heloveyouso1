from datetime import datetime
from py.xml import html
import pytest


def pytest_configure(config):
    # 添加接口地址与项目名称
    config._metadata["项目名称"] = "rc组专用接口"
    config._metadata['接口地址'] = 'rc组专用接口'
    # 删除Java_Home
    # config._metadata.pop("JAVA_HOME")


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    prefix.extend([html.p("所属部门: rc验收组")])
    prefix.extend([html.p("测试人员: 中华儿女")])


# @pytest.mark.optionalhook
# def pytest_html_results_table_header(cells):
#     cells.insert(1, html.th('Description'))
#
#
# @pytest.mark.optionalhook
# def pytest_html_results_table_row(report, cells):
#     cells.insert(1, html.td(report.description))
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))

    cells.insert(3, html.th('Time', class_='sortable time', col='time'))

    cells.pop()


def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))

    cells.insert(3, html.td(datetime.utcnow(), class_='col-time'))

    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield

    report = outcome.get_result()

    report.description = str(item.function.__doc__)

    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")  # 设置编码显示中文


@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    if report.passed:
        out = yield
        # 3. 从钩子方法的调用结果中获取测试报告
        # report = out.get_result()
        del data[:]
        # data.append(html.div(report.description, class_='empty log'))
        # data.append(html.div(report, class_='empty log'))
        data.append(html.div("秀儿",class_='log'))


# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     print('------------------------------------')
#
#     # 获取钩子方法的调用结果
#     out = yield
#     print('用例执行结果', out)
#
#     # 3. 从钩子方法的调用结果中获取测试报告
#     report = out.get_result()
#
#     print('测试报告：%s' % report)
#     print('步骤：%s' % report.when)
#     print('nodeid：%s' % report.nodeid)
#     print('description:%s' % str(item.function.__doc__))
#     print(('运行结果: %s' % report.outcome))