import os
import sys
import asyncio
import aiohttp
import queue
import sys

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

# 定义一个json队列
tasks = []

# 信号量
sem = asyncio.Semaphore(50)


# 申请书
async def fetch_async(body, qq_id):
    async with sem:
        async with aiohttp.ClientSession() as session:
            try:
                log.get_log("async_handle_authorization", "INFO", "入参:{}".format(body))
                async with session.post(url=url, data=json.dumps(body)) as resp:
                    re = await resp.json()
                    log.get_log("async_handle_authorization", "INFO", "返参:{}".format(re))
                    if re['errno'] == "0":
                        claim_authorization.update_status(back_qq_id=qq_id,
                                                          authorization_url=re['data']['claimAuthUrl'])
                    else:
                        print(11111)
            except Exception as e:
                print("API请求失败:", e)


url = "http://claim.equity.module.turboradio.cn/api/claimAuth/make"
claim_auth = claim_authorization.get_authorization_date()
sex = "男"
for i in claim_auth:
    if i[6] is None:
        continue
    body = {}
    if (int(i[6][-2]) % 2) == 0:
        sex = "女"
    body["accountName"] = i[0]
    body["bankAccount"] = i[1]
    body["companyName"] = "上海聚音信息科技有限公司"
    body['damageAddress'] = i[3]
    body['damageTime'] = i[4]
    body['date'] = "2022-07-15"
    body['insuredIdNo'] = i[6]
    body['insuredIdNoAddress'] = i[7]
    body['insuredIdNoEndDate'] = i[8]
    body['insuredIdNoStartDate'] = i[9]
    body['insuredName'] = i[10]
    body['insuredTelephone'] = i[11]
    body['isSeal'] = False
    body['openBankName'] = i[12]
    body['policyNo'] = i[13]
    body['sex'] = sex
    body['sign'] = i[14]
    body['systemCode'] = "FuDeDrug"
    body['telephone'] = "021-55099707"
    qq_id = i[-3]
    tasks.append(fetch_async(body, qq_id))
event_loop = asyncio.get_event_loop()
results = event_loop.run_until_complete(asyncio.gather(*tasks))
event_loop.close()
