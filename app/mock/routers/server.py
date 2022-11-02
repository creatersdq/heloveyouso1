from fastapi import APIRouter
from app.extensions import res_wrapper
from app.public.policy.server_sh import Server_Sh
from app.schems.policy.common import connDetail

router = APIRouter()


@router.post(
    "/common/server/sh/handle",
    tags=["服务器操作"]
)
async def policy_ssh_actions(items: connDetail) -> res_wrapper:
    s = Server_Sh(
        entry_name=items.serverDetail.entryName,
        dev=items.serverDetail.dev
    )
    res = {}
    if items.serverLogDetail:
        # 读取服务器日志
        try:
            res["serverTaskNo"] = s.server_task_no
            res["commResult"] = s.read_log(
                server_log_name=items.serverLogDetail.serverDirName,
                day_retrospective=items.serverLogDetail.daysRetrospective,
                read_comm=items.serverLogDetail.readComm
            )
            return res_wrapper.resp_200(data=res)
        except Exception as e:
            return res_wrapper.resp_200_error(message=e)
    else:
        # 执行自定义linux命令
        try:
            s.send(items.serverDetail.commList)
            res["serverTaskNo"] = s.server_task_no
            res["commResult"] = s.read_file()
            return res_wrapper.resp_200(data=res)
        except Exception as e:
            return res_wrapper.resp_200_error(message=e)
