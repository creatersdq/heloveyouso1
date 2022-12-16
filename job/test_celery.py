import json
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


if __name__ == "__main__":
    a = os.getcwd()
    # os.system("celery -A celery_job worker -l info")
    url = "http://jm-insure.turboradio.cn/bill/getClaimBill"
    body = {
        "billNo": "20220926100954"
    }
    body = json.dumps(body)
    r = {
        "url": url,
        "body": body
    }
    r_list = [r]
    # post.delay(request_list=r_list)
