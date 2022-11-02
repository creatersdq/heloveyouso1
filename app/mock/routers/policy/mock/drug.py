import json
import app

from fastapi import APIRouter
from fastapi import Response
from fastapi import Request

from app.extensions import res_wrapper
from app.public.policy.mock.ypb import Ypb
from app.public.policy.mock.common import data_base
from app.public.policy.mock.api import ApiBase
from app.schems.policy.mock import Mock_Detail, Switch, MockClaimData

router = APIRouter()
i_base = ApiBase()


@router.post(
    "/policy/mock/drug/data",
    tags=["药品保-投保&理赔数据Mock"]
)
async def policy_mock(items: Mock_Detail) -> res_wrapper:
    """
    mock数据处理
    :param items:
    :return:
    """
    p = Ypb(items.dev)
    # 返参
    res = {}

    # 订单数据mock
    if items.switchConfig.orderDataMock == Switch.on:
        try:
            # 资金池释放订单
            p.mock_pool_claim(items.orderDetail)
        except Exception as e:
            return res_wrapper.resp_200_error(message="资金池订单释放失败:{}".format(e))
        finally:
            # 实时查询资金池金额
            response = p.get_pool_amount(items.orderDetail)
            claim_amount = response["data"]["claimAmount"]
            res["policyList"] = p.pool_id_list
            res["claimAmount"] = claim_amount

    # 理赔数据mock
    if items.switchConfig.claimDataMock == Switch.on:
        try:
            p.mock_claim_data(items.claimDetail.policyNo)
        except Exception as e:
            return res_wrapper.resp_200_error(message="理赔数据mock失败:{}".format(e))
        finally:
            res["claimData"] = p.mock_claim_no_data

    # 发票数据mock
    if items.switchConfig.invoiceDataMock == Switch.on:
        try:
            # 若传入billNo，则以入参为准
            if items.claimDetail.billNoMock is not None:
                p.invoice_data_mock(items.claimDetail.billNoMock)
            else:
                p.invoice_data_mock()
        except Exception as e:
            return res_wrapper.resp_200_error(message="发票数据mock失败:{]".format(e))
        finally:
            res["invoiceData"] = p.data_invoice

    # 订单影像件数据mock
    if items.switchConfig.orderAttachmentDataMock == Switch.on:
        try:
            # 若传入billNo，则以入参为准
            if items.claimDetail.billNoMock is not None:
                await p.order_attachments_mock(app.gl_session, items.claimDetail.billNoMock)
            else:
                await p.order_attachments_mock(app.gl_session)
        except Exception as e:
            return res_wrapper.resp_200_error(message="订单影像件数据mock失败:{}".format(e))
        finally:
            res["orderAttachmentsData"] = p.mock_order_attachments_data

    # 批次报案收款人信息和反洗钱信息数据mock
    if items.switchConfig.claimPayInfoMock == Switch.on:
        try:
            p.claim_pay_info_mock()
        except Exception as e:
            return res_wrapper.resp_200_error(message="批次报案收款人信息和反洗钱信息数据mock失败:{}".format(e))
        finally:
            res["claimPayInfoData"] = "success"

    return res_wrapper.resp_200(data=res)


@router.post(
    "/policy/mock/drug/claim_payments",
    tags=["赔案流水数据mock"]
)
async def claim_mock(items: MockClaimData) -> res_wrapper:
    try:
        data_base(
            dev=items.mockDev,
            num=items.mockNum
        )
        return res_wrapper.resp_200(data='success')
    except Exception as e:
        return res_wrapper.resp_200_error(message='error:{}'.format(e))


@router.post(
    "/policy/mock/drug/api/insure",
    tags=["mock-保司投保接口-标准返回"]
)
async def policy_insure_interface(request: Request):
    # 获取请求入参
    request_body = await request.body()
    # 返参处理
    data_xml = i_base.insure_data_del(request_body)

    headers = {"Content-Type": "application/xml"}
    return Response(
        content=data_xml,
        media_type="application/xml",
        headers=headers
    )


@router.post(
    "/policy/mock/drug/api/claim",
    tags=["mock-保司理赔接口-标准返回"]
)
async def policy_claim_interface(request: Request) -> res_wrapper:
    # 获取请求入参
    request_body = await request.body()
    # 返参处理
    data_xml = i_base.claim_data_del(request_body)
    headers = {"Content-Type": "application/xml"}
    return Response(
        content=data_xml,
        media_type="application/xml",
        headers=headers
    )
