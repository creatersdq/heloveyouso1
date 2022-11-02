import os
import yaml


def read_case_data(
        data_dir: str
) -> any:
    """
    获取配置文件数据
    :param data_dir: ../app/public/data/路径下配置文件名
    :return:
    """
    # 根路径
    root_base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    # 读取yml文件内容
    with open(
            os.path.join(root_base_dir, data_dir),
            'r',
            encoding="utf-8"
    ) as f:
        data = yaml.safe_load(f)
        return data


if __name__ == "__main__":
    res = read_case_data('cn_ud_test_mock/app/core/mock_db_common.yml')
    # res = read_case_data('cn_ud_test_mock/app/core/mock_data.yml')
    print(res, type(res))
