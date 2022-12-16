import os
import yaml
from core.conf import setting


# 获取yml文件的接口入参内容


def file_yml(yml_dir):
    project_path = os.path.dirname(os.path.dirname(__file__))
    with open("{}/cases/common/{}".format(project_path, yml_dir), "r", encoding="utf-8") as f:
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