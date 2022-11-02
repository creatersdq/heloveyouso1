from pydantic.main import BaseModel
from enum import Enum
from typing import Optional


class DEV(str, Enum):
    """
    环境
    """
    test = 'test'
    rc = 'rc'


class Switch(int, Enum):
    """
    mock数据开关
    """
    on = 1  # 执行
    off = 0  # 不执行


class SwitchConfig(BaseModel):
    """
    mock数据开关
    """
    orderDataMock: Switch = 0  # 订单数据mock, 0:不处理，1：处理
    claimDataMock: Switch = 0  # 理赔数据mock, 0:不处理，1：处理
    invoiceDataMock: Switch = 0  # 发票数据mock, 0:不处理，1：处理
    orderAttachmentDataMock: Switch = 0  # 影像件mock, 0:不处理，1：处理
    claimPayInfoMock: Switch = 0  # 批次报案收款人信息和反洗钱信息, 0:不处理，1：处理
    orderRecordsMock: Switch = 0  # 订单记录mock , 0:不处理，1：处理


class OrderDetail(BaseModel):
    """
    订单数据mock自定义配置
    """
    directPay: Optional[int]  # 订单是否直赔 0：否，1：是
    drugType: Optional[int]  # 药品类型：0 普药、1 特药、2 其他
    latitude: Optional[int] = 1  # 是否结算单模式：1、订单 2结算单
    retrospectNum: Optional[int] = -1  # 向前追溯期
    insureGroupId: Optional[int] = 7  # 投保组织ID 默认上海聚音：7
    medicalDeviced: Optional[int] = 0  # 是否含有医疗器械，0：不含，1：含
    specialDiseased: Optional[int] = 0  # 是否专病险，0：否、1：是
    specialDiseaseType: Optional[int] = 0  # 专病险类型，0：无 、1：护肝险、2：护肾险、3：糖尿病险、4：高血压险、5：高血脂险
    isAdditional: Optional[int] = None  # 是否陪投， 0：不陪投，1：陪投
    gear: Optional[int] = 0  # 档位
    sumClaim: Optional[float] = 2100  # 总保费
    totalNumber: Optional[int] = 3  # 总人数


class ClaimDetail(BaseModel):
    """
    理赔数据mock自定义配置
    """
    policyNo: Optional[str]  # 关联保单号
    orderAttachmentType: Optional[list] = [1, 2, 3,
                                           4]  # 影像件数据类型 ,1:身份证正面 2:身份证反面 3:处方 4:电子签名 5:下单确认页
    # 6:订单完成页 7:医师资格证书  8:中医（专长）医师资格证书 9:履约完成页 10:理赔授权书 11:发票 99:其他类型

    billNoMock: Optional[str] = 0  # 自定义批次号
    billNoNum: Optional[int] = 3  # 批次报案数量
    billNoAmount: Optional[float] = 200  # 批次报案金额
    isDirectPay = 0  # 是否直赔，0：非直赔，1：直赔（policy-claim_payinfo表数据）


class Mock_Detail(BaseModel):
    """
    mock数据配置信息
    """
    switchConfig: SwitchConfig
    dev: DEV
    orderDetail: OrderDetail
    claimDetail: ClaimDetail


class MockClaimData(BaseModel):
    """
    批量mock-claim_sub_records&payment_records表数据
    """
    mockDev: Optional[str]
    mockNum: Optional[int]


class GuaranteeDataMock(BaseModel):
    """
    mock保障订单理赔数据配置
    """
    productCode: Optional[str]
    claimPayMode: Optional[int]
    paymentType: Optional[int] = 2
    dev: Optional[str] = "rc"
    mockNum: Optional[int] = 1
