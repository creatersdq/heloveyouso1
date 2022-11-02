import os

# unify的基本路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 存放日志的路径
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# 存放测试数据的路径
CASE_DATA_DIR = os.path.join(BASE_DIR, 'excel_datas')

# 存放报告的路径
REPORT_DATA_DIR = os.path.join(BASE_DIR, 'report')

# if __name__ == '__main__':
#     print(BASE_DIR)
#     print(LOG_DIR)
#     print(CASE_DATA_DIR)
#     print(REPORT_DATA_DIR)
