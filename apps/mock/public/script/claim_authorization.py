import os
import sys
import asyncio
import aiohttp

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

url = "http://claim.equity.module.uniondrug.net/api/claimAuth/make"
claim_auth = claim_authorization.get_authorization_date()
body = {}
sex = "男"
for i in claim_auth:
    if (int(i[6][-2]) % 2) == 0:
        sex = "女"
    body["accountName"] = i[0]
    body["bankAccount"] = i[1]
    body["companyName"] = "上海聚音信息科技有限公司"
    body['damageAddress'] = i[3]
    body['damageTime'] = i[4]
    body['date'] = "2022-06-24"
    body['insuredIdNo'] = i[6]
    body['insuredIdNoAddress'] = i[7]
    body['insuredIdNoEndDate'] = i[8]
    body['insuredIdNoStartDate'] = i[9]
    body['insuredName'] = i[10]
    body['insuredTelephone'] = i[11]
    body['isSeal'] = True
    body['openBankName'] = i[12]
    body['policyNo'] = i[13]
    body['sex'] = sex
    body['sign'] = i[14]
    body['systemCode'] = "FuDeDrug"
    body['telephone'] = "021-55099707"
    print(111)
    try:
        log.get_log("handle_authorization", "INFO", "入参:{}".format(body))
        print(body)
        re = requests.post(url=url, data=json.dumps(body))
        log.get_log("handle_authorization", "INFO", "返参:{}".format(re.json()))
        if re.json()['errno'] == "0":
            claim_authorization.update_status(back_qq_id=i[-3], authorization_url=re.json()['data']['claimAuthUrl'])
        else:
            pass
    except Exception as e:
        print("API请求失败:", e)
