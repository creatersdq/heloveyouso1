from sqlalchemy import Column, String, Integer, Float, DateTime, Date, Text, DECIMAL,VARCHAR
from apps.core.data_base import Base
from apps.core.timestamp_mixin import TimestampMixin


class PolicyObject(Base):
    __tablename__ = 'policy_object'  # 表名  投保标的信息
    # __table_args__ = {'schema': 'cn_uniondrug_module_equity_claim_new2'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    waterNo = Column(String)  # 南京投保批次号
    equityNo = Column(String)  # 投保码
    insuredName = Column(String)  # 姓名
    insuredIdNo = Column(String)  # 身份证号
    premium = Column(Float)  # 保费
    amount = Column(Float)  # 保额
    gmtCreated = Column(DateTime)
    gmtUpdated = Column(DateTime)
    startDate = Column(DateTime)  # 身份证起期
    endDate = Column(DateTime)  # 身份证止期
    phone = Column(String)  # 手机号
    address = Column(String)  # 身份证地址


class PolicyRecords(Base):
    __tablename__ = 'policy_records'  # 表名  投保记录表
    # __table_args__ = {'schema': 'cn_uniondrug_module_equity_claim_new2'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    waterNo = Column(String)  # 南京批次号
    taskNo = Column(String)  # 投保任务单号
    batchId = Column(Integer)  # policy_batch_records 主键id
    bsBranchId = Column(Integer)  # 承保保司机构主键ID
    bsProductId = Column(Integer)  # 保司产品表主键Id
    bsSaleId = Column(Integer)  # 保司端销售id
    qdProductId = Column(Integer)  # 渠道产品主键id
    policyNo = Column(String)  # 保单号
    systemCode = Column(String)  # 出单系统标识
    businessDepartmentCode = Column(String)  # 归属机构代码
    companyName = Column(String)  # 保司机构名称
    claimRuleId = Column(Integer)  # 理赔规则主键ID
    sumPremium = Column(Float)  # 总保费
    sumAmount = Column(Float)  # 总保额
    sumPremiumPaid = Column(Float)  # 已支付保费
    sumClaim = Column(Float)  # 已报案金额
    sumClaimed = Column(Float)  # 已核赔金额
    sumClaimPaid = Column(Float)  # 已收赔款
    totalNum = Column(Integer)  # 服务人数
    isPolicyOnline = Column(Integer)  # 投保方式 1:线下 2:线上
    claimRate = Column(Float)  # 理赔上限比例（赔付率）
    serFeeRate = Column(Float)  # 信息服务费比例
    ageFeeRate = Column(Float)  # 代理手续费比例
    healthFeeRate = Column(Float)  # 健康管理费比例
    status = Column(Integer)  # 投保状态 0关闭（暂停理赔通道）  1生效（投保成功） 2完成（保单已理赔完）
    startDate = Column(DateTime)  # 保单生效日


class PolicyBatchRecords(Base):
    __tablename__ = 'policy_batch_records'  # 表名  保单批次待投记录表
    # __table_args__ = {'schema': 'cn_uniondrug_module_equity_claim_new2'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    waterNo = Column(String)  # 南京投保批次号
    taskNo = Column(String)  # 投保单编码
    bsBranchId = Column(Integer)  # 商户编码
    bsProductId = Column(Integer)  # 保司产品表主键id
    qdCooperationId = Column(Integer)  # qd_cooperation表主键id
    bsSaleId = Column(Integer)  # 保司端销售id
    qdProductId = Column(Integer)  # 渠道产品表主键id
    qdSaleId = Column(Integer)  # 销售表主键Id
    companyName = Column(String)  # 保司机构名称
    sumPremium = Column(Float)  # 总保费
    sumAmount = Column(Float)  # 总保额
    claimRate = Column(Float)  # 理赔上限比例
    sumClaim = Column(Float)  # 赔付金额
    serFeeRate = Column(Float)  # 信息服务费比例
    ageFeeRate = Column(Float)  # 代理手续费比例
    healthFeeRate = Column(Float)  # 健康管理费比例
    startDate = Column(DateTime)  # 起保日期
    endDate = Column(DateTime)  # 终保日期
    insureDate = Column(DateTime)  # 投保/签单日期
    totalNum = Column(Integer)  # 标的数量
    comment = Column(String)  # 驳回备注
    processInstanceId = Column(String)  # 钉钉审批流水号
    systemStatus = Column(Integer)  # 系统状态： 1:承保审核中，2: 承保驳回， 3:保单审核中， 4 保单审核驳回  5 投保失败 6 已完成
    businessStatus = Column(Integer)  # 业务状态。1:盖章审核中，2: 盖章驳回， 3:盖章已完成
    origin = Column(Integer)  # 渠道  1: 线下 2: 线上 3:投保单投保
    gmtCreated = Column(DateTime)
    gmtUpdated = Column(DateTime)


class PolicyFileRecords(Base):
    __tablename__ = 'policy_file_records'  # 表名  保单文件记录表
    # __table_args__ = {'schema': 'cn_uniondrug_module_equity_claim_new2'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    batchId = Column(Integer)  # policy_batch_records主键id
    policyNo = Column(String)  # 保单号
    dataFileUrl = Column(String)  # 南京投保文件线上地址
    proposalFileUrl = Column(String)  # 投保单原件
    proposalStampFileUrl = Column(String)  # 投保单签章件
    policyFileUrl = Column(String)  # 投保文件线上地址(与保司交互)
    epolicyUrl = Column(String)  # 电子保单下载地址
    claimStampFileUrl = Column(String)  # 盖章理赔材料（保单维度）
    gmtCreated = Column(DateTime)  #
    gmtUpdated = Column(DateTime)  #
    ossEpolicyUrl = Column(String)  # 电子保单上传oss
    invoiceUrl = Column(String)  # 电子发票下载地址
    paymentUrl = Column(String)  # 保单缴费通知书下载地址


class PolicyPayPlan(Base):
    __tablename__ = 'policy_pay_plan'  # 表名  保单付款计划表
    # __table_args__ = {'schema': 'cn_uniondrug_module_equity_claim_new2'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID


class PolicyPlanLog(Base):
    __tablename__ = 'policy_plan_log'  # 表名  投保分流日志表
    # __table_args__ = {'schema': 'cn_uniondrug_module_equity_claim_new2'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    qdCooperationId = Column(String)  # qd_cooperation 表主键id
    qdPolicyPlanRuleId = Column(String)  # 投保分流规则表主键id
    qdPolicyPlanDetailId = Column(String)  # 保单详情表主键id
    date = Column(String)  # 日期
    qdSaleId = Column(String)  # 销售主键id
    planRate = Column(String)  # 计划分流比例
    claimRate = Column(String)  # 赔付率
    amount = Column(String)  # 可投保总额
    actualAmount = Column(String)  # 实际分配值
    sumPremium = Column(String)  # 保费
    gmtCreated = Column(DateTime)
    gmtUpdated = Column(DateTime)


class BsSaleRecords(Base):
    __tablename__ = 'bs_sale_records'  # 表名  投保分流日志表
    # __table_args__ = {'schema': 'cn_uniondrug_module_equity_claim_new2'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    bsProductId = Column(Integer)
    bsBranchId = Column(Integer)
    policyRuleId = Column(Integer)
    claimRuleId = Column(Integer)
    claimMaterialId = Column(Integer)
    claimTemplateId = Column(Integer)
    businessDepartmentCode = Column(Integer)
    systemConfigId = Column(Integer)
    status = Column(Integer)


class PolicyRule(Base):
    __tablename__ = 'policy_rule'  # 表名  投保规则表
    # __table_args__ = {'schema': 'cn_uniondrug_module_equity_claim_new2'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    isPolicyOnline = Column(Integer)
    insuredMaxAge = Column(Integer)
    insuredMinAge = Column(Integer)
    insuredSex = Column(Integer)
    claimTopAmount = Column(Integer)
    payTypes = Column(String)
    premiumPeriod = Column(Integer)
    latitude = Column(Integer)


class BsProducts(Base):
    __tablename__ = 'bs_products'  # 表名  投保规则表
    # __table_args__ = {'schema': 'cn_uniondrug_module_equity_claim_new2'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    bsBranchId = Column(Integer)
    riskId = Column(Integer)
    insuranceNature = Column(Integer)
    productName = Column(String)
    insuranceCode = Column(String)
    policyRuleId = Column(String)
    claimRuleId = Column(Integer)
    claimMaterialId = Column(Integer)
    claimTemplateId = Column(Integer)
    status = Column(Integer)
    policyPeriod = Column(Integer)
    policyPeriodType = Column(Integer)
    startRetrospectNum = Column(Integer)
    effectNum = Column(Integer)
    systemConfigId = Column(Integer)


class BsProductsRation(Base):
    __tablename__ = 'bs_product_ration'  # 表名  产品方案详情表
    # __table_args__ = {'schema': 'cn_uniondrug_module_equity_claim_new2'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    bsProductId = Column(Integer)
    bsDutyId = Column(Integer)
    rationCode = Column(Integer)
    premium = Column(Float)
    premiumRate = Column(Float)
    amount = Column(Float)
    rationType = Column(Integer)
    limitQuantity = Column(Integer)
    calcPremiumRate = Column(Float)


class ClaimRecords(Base):
    __tablename__ = 'claim_records'  # 表名  出险记录表
    # __table_args__ = {'schema': 'cn_uniondrug_module_equity_claim_new2'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    batchId = Column(Integer)
    billNo = Column(String)
    orderNo = Column(String)
    userName = Column(String)
    damageNo = Column(String)
    policyNo = Column(String)
    storeName = Column(String)
    certificateNo = Column(String)
    damageAmount = Column(Float)
    partnerName = Column(String)
    partnerCode = Column(String)
    gmtCreated = Column(DateTime)


class OrderAttachments(Base):
    __tablename__ = 'order_attachments'  # 表名  订单影像件扩展信息表
    # __table_args__ = {'schema': 'cn_uniondrug_module_equity_claim_new2'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    orderNo = Column(String)
    fileType = Column(String)
    fileUrl = Column(String)


class ClaimBatchRecords(Base):
    __tablename__ = 'claim_batch_records'  # 表名  理赔批次表
    # __table_args__ = {'schema': 'cn_uniondrug_module_equity_claim_new2'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    policyNo = Column(String)
    systemCode = Column(String)
    totalNum = Column(Integer)
    totalAmount = Column(Float)
    sumClaim = Column(Float)
    sumClaimed = Column(Float)
    sumClaimPaid = Column(Float)
    status = Column(Integer)
    billNo = Column(String)


class BranchConfig(Base):
    __tablename__ = 'branch_config_1'  # 通用保司配置表
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    bsProductId = Column(Integer)
    bsBranchParentId = Column(Integer)
    insureUrl = Column(String)
    claimUrl = Column(String)
    invoiceUrl = Column(String)
    payInfoUrl = Column(String)
    secretkey = Column(String)
    imageInvoiceUrl = Column(String)
    riskCode = Column(String)
    rationType = Column(String)
    kindCode = Column(String)
    amount = Column(Float)
    premium = Column(Float)
    damageReasonCode = Column(String)
    damageReasonName = Column(String)


class SystemConfig(Base):
    __tablename__ = 'system_config'  # 系统配置表
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    policyChannel = Column(String)
    claimChannel = Column(String)
    claimAuthChannel = Column(String)
    claimMaterialChannel = Column(String)
    imageUploadChannel = Column(String)
    proposalChannel = Column(String)
    systemName = Column(String)
    comment = Column(String)
    isPolicyOnline = Column(Integer)
    isAsynchronous = Column(Integer)
    status = Column(Integer)


class BsBranch(Base):
    __tablename__ = 'bs_branch'  # 保司机构表
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    companyName = Column(String)
    companyShortName = Column(String)
    cooperationCode = Column(String)
    cooperationId = Column(Integer)
    provinceName = Column(String)
    cityName = Column(String)
    address = Column(String)
    linkerMobile = Column(String)
    parentId = Column(Integer)
    status = Column(Integer)
    dutyPerson = Column(String)


class PolicyDetail(Base):
    __tablename__ = 'policy_detail'  # 保单详情表
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    policyId = Column(Integer)
    companyName = Column(String)
    startDate = Column(String)
    endDate = Column(String)
    insureDate = Column(String)
    sumAmount = Column(Float)
    sumPremium = Column(Float)
    applicantName = Column(String)
    applicantIdNo = Column(String)
    applicantAddress = Column(String)
    insuredName = Column(String)
    insuredIdNo = Column(String)
    insuredAddress = Column(String)
    linkerName = Column(String)
    linkerMobile = Column(String)
    linkerEmail = Column(String)
    endRetrospectNum = Column(Integer)
    startRetrospectNum = Column(Integer)
    statementId = Column(Integer)
    paymentMethod = Column(Integer)
    specialDiseaseType = Column(Integer)
    retrospectNum = Column(Integer)
    effectNum = Column(Integer)
    statementBillId = Column(Integer)


class ClaimSubRecords(Base):
    __tablename__ = 'claim_sub_records'  # 报案表
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    batchId = Column(Integer)
    waterNo = Column(String)
    registNo = Column(String)
    policyNo = Column(String)
    claimPayNo = Column(String)
    systemCode = Column(String)
    partnerCode = Column(String)
    totalNum = Column(Integer)
    totalAmount = Column(Float)
    sumClaim = Column(Float)
    sumClaimed = Column(Float)
    sumClaimPaid = Column(Float)
    claimTime = Column(DateTime)
    claimedTime = Column(DateTime)
    claimPaidTime = Column(DateTime)
    status = Column(String)
    failReason = Column(String)
    dataFileUrl = Column(String)
    claimStampFileUrl = Column(String)
    gmtCreated = Column(DateTime)
    gmtUpdated = Column(DateTime)


class PaymentRecords(Base):
    __tablename__ = 'payment_records'  # 保单的资金流动表
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    policyNo = Column(String)
    registNo = Column(String)
    refNo = Column(String)
    claimPayNo = Column(String)
    voucherNo = Column(String)
    tradeAmount = Column(Float)
    tradeDate = Column(Date)
    tradeTime = Column(DateTime)
    ugAcctNo = Column(String)
    acctName = Column(String)
    acctNo = Column(String)
    acctBankNode = Column(String)
    acctBankName = Column(String)
    acctType = Column(String)
    feeType = Column(String)
    reportFileUrl = Column(String)
    status = Column(Integer)
    comment = Column(String)
    gmtCreated = Column(DateTime)
    gmtUpdated = Column(DateTime)
    floatConfigId = Column(Integer)
    branchId = Column(Integer)
    qdSaleId = Column(Integer)


class ClaimPayInfo(Base):
    __tablename__ = 'claim_payinfo'  # 批次报案收款人信息和反洗钱信息
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    batchId = Column(Integer)
    partnerCode = Column(String)
    acctName = Column(String)
    acctNo = Column(String)
    acctBankName = Column(String)
    acctBranchName = Column(String)
    acctBranchNode = Column(String)
    provinceName = Column(String)
    provinceCode = Column(String)
    cityName = Column(String)
    cityCode = Column(String)
    businessScope = Column(Text)
    businessEndDate = Column(String)
    businessStartDate = Column(String)
    businessAddress = Column(String)
    businessNumber = Column(String)
    partnerName = Column(String)
    payeeIdNoEndDate = Column(String)
    payeeIdNoStartDate = Column(String)
    payeeIdNoUrl = Column(String)
    payeeName = Column(String)
    payeeIdNo = Column(String)
    payeeMobile = Column(String)
    payeeAddress = Column(String)
    businessLicense = Column(String)
    payeeIdNoFront = Column(String)
    payeeIdNoBack = Column(String)


class QdPolicyPlanExtra(Base):
    __tablename__ = 'qd_policy_plan_extra'  # 投保分流补充表
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    qdPolicyPlanRuleId = Column(Integer)
    drugType = Column(Integer)
    payType = Column(Integer)
    rate = Column(DECIMAL)
    isMedicalDeviced = Column(Integer)


class QdPolicyPlanRule(Base):
    __tablename__ = 'qd_policy_plan_rule'  # 投保分流计划表
    id = Column(Integer, primary_key=True, unique=True)  # 主键ID
    qdCooperationId = Column(Integer)
    planRuleName = Column(VARCHAR)
    status = Column(Integer)
