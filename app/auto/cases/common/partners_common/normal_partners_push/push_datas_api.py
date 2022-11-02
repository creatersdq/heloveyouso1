from apps.extensions.read_yml import file_yml
from apps.extensions.logger import log
import requests
import json
'''
请求数据推送接口
'''
class DataPush:

    def __init__(self):
        self.partners_push = file_yml("partners_common/datas/partners_data_push.yml")
        self.headers = self.partners_push["headers"]

    def push_request(self,data):

        url = self.partners_push["push_data"]["url"]
        try:
            resp = requests.post(url=url, data=json.dumps(data), headers=self.headers)
            res = resp.json()
            log.get_log("partners_push_datas/request", "INFO", "{},{},{}".format(url, data, res))
            return res, url, data, self.headers

        except Exception as e:
            print("库存查询接口异常,ERROR", e)
            log.get_log("partners_push_datas/request", "DEBUG", "{},{},{}".format(url, data, e))
            return False