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
from app.curd import claim_authorization
from app.extensions.logger import log

sem = asyncio.Semaphore(50)


async def fetch_async(body, qq_id):
    async with sem:
        async with aiohttp.ClientSession() as session:
            try:
                log.get_log("async_handle_power", "INFO", "入参:{}".format(body))
                async with session.post(url=url, data=json.dumps(body)) as resp:
                    re = await resp.json()
                    log.get_log("async_handle_power", "INFO", "返参:{}".format(re))
                    if re['errno'] == "0":
                        claim_authorization.update_sq_status(qq_id=qq_id, power_url=re['data']['claimAuthUrl'])
                    else:
                        print("接口异常！！！")
            except Exception as e:
                print("API请求失败:", e)


url = "http://claim.equity.module.turboradio.cn/api/claimAuth/zhongcheng"
claim_auth = claim_authorization.get_power_date()
body = {}
tasks = []
sex = "男"
for i in claim_auth:
    body["name"] = i[1]
    body["idCard"] = i[0]
    body["policyNo"] = i[2]
    body['partnerName'] = 1
    body['partnerAcctBankName'] = "招商银行上海分行大连路支行"
    body['partnerAcctName'] = 1
    body['partnerAcctNo'] = "121909738010403"
    body['signUrl'] = i[3]
    qq_id = i[-2]
    tasks.append(fetch_async(body, qq_id))

event_loop = asyncio.get_event_loop()
results = event_loop.run_until_complete(asyncio.gather(*tasks))
event_loop.close()
