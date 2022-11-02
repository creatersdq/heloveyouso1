import os
import sys
import time

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.append(curPath)
project = "cn_ud_test_mock"
sys.path.append(os.getcwd().split(project)[0] + project)
import requests
import json
from apps.curd import claim_authorization
from apps.extensions.logger import log

url = "http://claim.equity.module.turboradio.cn/api/claimAuth/zhongcheng"
claim_auth = claim_authorization.get_power_date()
sex = "男"
for i in claim_auth:
    body = {}
    body["name"] = i[1]
    body["idCard"] = i[0]
    body["policyNo"] = i[2]
    body['partnerName'] = 1
    body['partnerAcctBankName'] = "招商银行上海分行大连路支行"
    body['partnerAcctName'] = 1
    body['partnerAcctNo'] = "121909738010403"
    body['signUrl'] = i[3]
    try:
        log.get_log("handle_power", "INFO", "入参:{}".format(body))
        re = requests.post(url=url, data=json.dumps(body))
        log.get_log("handle_power", "INFO", "返参:{}".format(re.json()))
        if re.json()['errno'] == "0":
            claim_authorization.update_sq_status(qq_id=i[-2], power_url=re.json()['data']['claimAuthUrl'])
        else:
            print("接口异常:{}".format(re.text))
        time.sleep(0.5)
    except Exception as e:
        print("API请求失败:", e)
