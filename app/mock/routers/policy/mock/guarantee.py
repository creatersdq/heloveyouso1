from fastapi import APIRouter

from app.extensions import res_wrapper
from app.public.policy.mock.guarantee import Guarantee
from app.schems.policy.mock import GuaranteeDataMock

router = APIRouter()


@router.post(
    "/policy/mock/guarantee/data",
    tags=["保障-订单&理赔数据mock"]
)
async def claim_mock(items: GuaranteeDataMock) -> res_wrapper:
    g = Guarantee(dev=items.dev)
    res = []
    for i in range(items.mockNum):
        data = {}
        try:
            a = g.order_data_mock(
                product_code=items.productCode,
                claim_pay_mode=items.claimPayMode
            )
            if a["errno"] == "0":
                data["orderNo"] = g.data_guarantee["order_no"]
                b = g.claim_data_mock(
                    product_code=items.productCode,
                    claim_pay_mode=items.claimPayMode,
                    payment_type=items.paymentType
                )
                if b["errno"] == "0":
                    data["inRegistNo"] = b["data"]["inRegistNo"]
                else:
                    data["mock_result"] = "理赔数据推送失败:{}".format(b["error"])
            else:
                data["mock_result"] = "订单数据推送失败:{}".format(a["error"])
            res.append(data)
        except Exception as e:
            return res_wrapper.resp_200_error(message='error:{}'.format(e))
    return res_wrapper.resp_200(data=res)
