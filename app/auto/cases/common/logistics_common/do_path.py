import os

# 跟路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# 存放日志的路径
LOG_DIR = os.path.join(BASE_DIR, 'case_logs')

# 存放测试数据的路径
CASE_DATA_DIR = os.path.join(BASE_DIR, 'cases/common/logistics_common/datas')

if __name__ == '__main__':
    print(BASE_DIR)
    print(LOG_DIR)
    print(CASE_DATA_DIR)
