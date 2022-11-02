import asyncio
import json

from app.curd.policy.crud_insure import get_claim_records
from app.extensions.logger import log


async def fetch_async(request_body, request_url, session) -> any:
    """
    异步http请求
    :param session:
    :param request_body: 入参
    :param request_url: url+api
    :return:
    """
    try:
        header = {"Content-Type": "application/json"}
        log.get_log("info", "INFO", "API:{}".format(request_url))
        log.get_log("info", "INFO", "入参:{}".format(request_body))
        async with session.post(url=request_url, data=json.dumps(request_body), headers=header) as resp:
            re = await resp.json()
            log.get_log("info", "INFO", "返参:{}".format(re))
    except Exception as e:
        log.get_log("info", "INFO", "API请求失败:{}".format(e))


if __name__ == "__main__":
    # 定义一个json队列
    tasks = []
    # 信号量
    sem = asyncio.Semaphore(50)
    url = "http://claim.equity.module.turboradio.cn/order/attachment"
    claim_data = get_claim_records(28833, "test")
    body = None

    for i in claim_data:
        c = i.orderNo
        body1 = {
            "orderNo": "20220725774153681753",
            "userName": "樊战岗",
            "idcardNo": "610523199201086936",
            "idcardStartDate": "2022-07-01 00:00:00",
            "idcardEndDate": "2122-07-01 00:00:00",
            "idcardAddress": "",
            "partnerName": "国药控股国大药房上海连锁有限公司",
            "partnerCode": "国药控股国大药房上海连锁有限公司",
            "storeName": "国药控股国大药房上海连锁有限公司",
            "storeCode": "2018090300758953701297",
            "storeAddress": "江苏省南京市浦口区江苏省南京市雨花台区铁心桥街道金证南京科技园",
            "attachments": [
                {
                    "fileType": 1,
                    "fileUrl": "http://uniondrug-release.oss-cn-shanghai.aliyuncs.com/frontend.wx/tvkan9keasikossitf6vbje6hl.jpeg"
                },
                {
                    "fileType": 2,
                    "fileUrl": "http://uniondrug-release.oss-cn-shanghai.aliyuncs.com/frontend.wx/rmfmldl1vcl172mjvhd77uea7o.jpeg"
                },
                {
                    "fileType": 4,
                    "fileUrl": "https://uniondrug-release.oss-cn-shanghai.aliyuncs.com/frontend.wx/3ppse69sdscn8hqnol1k9fm9gq.png"
                }
            ],
            "guardianInfo": {
                "name": "",
                "idcardNo": ""
            }
        }
        # body = json.dumps(body1)
        print(type(body1))
        tasks.append(fetch_async(body1, url))

    event_loop = asyncio.get_event_loop()
    results = event_loop.run_until_complete(asyncio.gather(*tasks))
    event_loop.close()
