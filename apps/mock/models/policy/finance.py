from sqlalchemy import Column, String, Integer, DateTime, Float, DECIMAL
from apps.core.data_base import Base


class Pool_Claim(Base):
    __tablename__ = 'pool_claim'  # 待理赔池
    __table_args__ = {'schema': 'cn_udm_insure'}  # 指定其他库名，同RDS
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    policy_id = Column(Integer)  # 保单ID
    code_id = Column(Integer)  # 投保码ID
    insurer_id = Column(Integer)  # 保司ID
    unit_id = Column(Integer)  # 核算单位ID
    partner_id = Column(Integer)  # 连锁ID
    statement_no = Column(String)  # 结算单号
    order_no = Column(String)  # 订单号
    gmt_paid = Column(DateTime)  # 订单时间
    equity_id = Column(Integer)  # Equity::id
    equity_no = Column(String)  # 权益卡号（已废弃）'
    member_name = Column(String)  # 会员名称
    member_id_card = Column(String)  # 会员身份证号
    premium = Column(Float)  # 保费（默认100，二要素投保后更新）
    insured_amount = Column(Float)  # 保额
    claim_amount = Column(Float)  # 理赔金额
    hx_status = Column(Integer)  # 订单是否含换新，0:无、1:有
    goods_replace = Column(Integer)  # 商品是否替换完成，0:未替换、1:已替换
    direct_pay = Column(Integer)  # 订单是否直赔 0：否，1：是
    certified = Column(Integer)  # 二要素认证结果，-1：认证不通过、0：不明、1：认证通过
    drug_type = Column(Integer)  # 药品类型：0 普药、1 特药、2 其他
    medical_deviced = Column(Integer)  # 是否含有医疗器械，0：不含，1：含
    special_diseased = Column(Integer)  # 是否专病险，0：否、1：是
    special_disease_type = Column(Integer)  # 专病险类型，0：无 、1：护肝险、2：护肾险、3：糖尿病险、4：高血压险、5：高血脂险
    gmt_plan_claimed = Column(String)  # 计划理赔时间（yyyy-MM-dd），当设定计划理赔时间，只有在计划理赔时间内，才可以参与理赔
    claim_status = Column(Integer)  # 理赔状态，-1 取消理赔、0 未理赔、1 理赔成功（已废弃）
    claim_fail_count = Column(Integer)  # 理赔失败次数（已废弃）
    insure_group_id = Column(Integer)  # 投保组织ID
    gmt_created = Column(DateTime)  # 创建时间
    gmt_updated = Column(DateTime)  # 更新时间


class Batch(Base):
    __tablename__ = 'batch'  # 报案批次
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    __table_args__ = {'schema': 'cn_udm_insure'}  # 指定其他库名，同RDS
    batch_no = Column(String)  # 唯一批次号
    order_count = Column(Integer)  # 订单数量
    sum_claimed_amount = Column(DECIMAL)  # 保单ID



