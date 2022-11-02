from fastapi import APIRouter

from apps.extensions import res_wrapper
from apps.public.policy.action import ActionBase
from apps.schems.policy.action import PolicyAction, ACTIONTYPE

router = APIRouter()


@router.post(
    "/policy/common/actions",
    tags=["药品保-常用操作模拟"]
)
async def policy_actions(items: PolicyAction) -> res_wrapper:
    p = ActionBase(items.dev)
    res = ''
    # 锁眼计划日志清理
    if items.type == ACTIONTYPE.policyLogReset:
        try:
            p.policy_log_action()
            res = "锁眼计划日志清理成功"
        except Exception as e:
            return res_wrapper.resp_200_error(message="锁眼计划日志清理失败:{}".format(e))
    # 影像件推送保司
    if items.type == ACTIONTYPE.imagePush:
        try:
            p.image_push(items.registNo)
            res = "影像件数据推送保司成功"
        except Exception as e:
            return res_wrapper.resp_200_error(message="影像件数据推送失败:{}".format(e))
    # 发票推送保司
    if items.type == ACTIONTYPE.invoicePush:
        try:
            p.invoice_push(items.registNo)
            res = "发票数据推送保司成功"
        except Exception as e:
            return res_wrapper.resp_200_error(message="发票数据推送失败:{}".format(e))

    return res_wrapper.resp_200(data=res)
