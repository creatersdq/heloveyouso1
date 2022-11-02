from apps.cases.common.insurance_common.do_read_yaml import read_case_data

# 读取配置文件
common_config = read_case_data('common.yaml')
server_config = read_case_data('server_data.yaml')


if __name__ == "__main__":
    print(common_config)
    print(server_config)
    print(type(server_config))
    print(server_config["SERVER_PATH_test"])


