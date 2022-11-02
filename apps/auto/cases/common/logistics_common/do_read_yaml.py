import os
import yaml

from apps.cases.common.logistics_common.do_path import CASE_DATA_DIR


def read_case_data(case_data_dir):
    """
    :param case_data_dir: 测试用例数据的文件名字
    :return:
    """
    with open(os.path.join(CASE_DATA_DIR,case_data_dir), 'r', encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data


if __name__ == "__main__":
    res=read_case_data('create_order_data.yaml')
    print(res,type(res))

