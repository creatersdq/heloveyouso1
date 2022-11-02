import os
from ruamel import yaml

'''
！并将字典格式的接口入参写入到yml文件，转化成yml的字典格式
！转换好格式后复制到存测试参数的yml文件中
'''

desired_caps = {
    "requestNo": "1",
    "payNoticeList": [
    {
       "memberId":15965886,
    	"mobile":"1515713331383",
        "bankCode": "1",
        "payStatus": "1",
        "orderAmount": 1,
        "equityAmount":100,
        "orderNo": "1",
        "couponId": "161069523948000011"
    }
 ]
}


cur_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(cur_path, "../../extensions/tools/new_yml.yml")

# 写入到yaml文件
with open(yaml_path, "w", encoding="utf-8") as f:
    yaml.dump(desired_caps, f, Dumper=yaml.RoundTripDumper, allow_unicode=True)



