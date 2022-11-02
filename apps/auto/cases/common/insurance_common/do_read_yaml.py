import os
import yaml

from apps.cases.common.insurance_common.do_path import CASE_DATA_DIR
from apps.extensions.logger import log


def read_case_data(case_data_dir: str) -> dict:
    """
    :param case_data_dir: 测试用例数据的文件名字
    :return:
    """
    with open(os.path.join(CASE_DATA_DIR, case_data_dir), 'r', encoding="utf-8") as f:
        data = yaml.safe_load(f)
        log.get_log("insurance", "INFO", "获取配置文件:{}".format(data))
        return data


if __name__ == "__main__":
    res = read_case_data('common.yaml')
    print(res, type(res))
