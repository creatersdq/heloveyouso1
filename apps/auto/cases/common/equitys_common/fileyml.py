import os
import yaml
from faker import Factory
import random
from apps.core.conf import setting
# 获取yml文件的接口入参内容



def file_yml():
    project_path = os.path.dirname(__file__)
    with open("{}/projects_data.yml".format(project_path), "r", encoding="utf-8") as f:
        file_data = f.read()
    files = yaml.safe_load(file_data)
    for k in files.keys():
        if setting()['ENV'] == "DEV":
            if 'url' in (files[k].keys()):
                a = files[k]['url'].replace("turboradio.cn", "uniondrug.net")
                files[k]['url'] = a
            else:
                pass
        else:
            pass

    return files

# 随机生成一个数值
def nam():
    fake = Factory.create("zh_CN")
    nam = fake.postcode()
    return nam


