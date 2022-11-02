import os
import yaml
from faker import Factory
import random

# 获取yml文件的接口入参内容
def logindata_yml():
    project_path = os.path.dirname(__file__)
    with open("{}/wxdata.yml".format(project_path), "r", encoding="utf-8") as f:
        file_data = f.read()
    files = yaml.safe_load(file_data)
    return files