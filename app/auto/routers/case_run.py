from fastapi import APIRouter, BackgroundTasks
from apps.extensions.logger import log
from apps.extensions import new_response_wrapper
from apps.schems.case_run import RunCase
from apps.db_actions.project import get_prj_status
from celery.result import AsyncResult
import requests
from ..worker.celery_app import celery_app
import json
from apps.core.conf import setting
from apps.new_run import run_case

router = APIRouter()


@router.post('/api/run')
async def xxx(item: RunCase, background_tasks: BackgroundTasks):
    prj_sta = get_prj_status(item.project)
    if prj_sta and prj_sta[0][0] == 1 and prj_sta[0][1] == 1:
        if item.ifCelery:
            return new_response_wrapper.resp_200("该功能正在研发中....")
        else:
            data = {"type": 1, "planName": item.project, "projectId": prj_sta[0][2], "needNo": 1}
            try:
                token = '38ccc84ca8cd6fa8688b851f26188d8684777994ccfc71e074742c0b863cd741'
                url = setting()['PLAN_ADDRESS']
                res = requests.post(url=url, data=json.dumps(data),
                                    headers={
                                        'token': token, "account": "18100000005"})
                log.get_log("conftest", "INFO", "返回参数json:{},返回参数text:{}".format(res.json(), res.text))
                plan_no = res.json()['data']["plan_no"]
            except Exception as e:
                plan_no = "livingzhuanyong"
            background_tasks.add_task(run_case, item.project, plan_no)
            # 使用celery启动自动化脚本
            # task = celery_app.send_task(
            #     'worker.celery_worker.async_run_scp', args=[item.project, plan_no], queue="auto-queue"
            # )

            return new_response_wrapper.resp_200()
    else:
        return new_response_wrapper.resp_200_error("项目类型错误或项目状态已停用")


@router.get('/api/run1')
def xxx():
    task = celery_app.send_task(
        'worker.celery_worker.add1', args=["商品上下家", "living1234567"]
    )
    return 1
