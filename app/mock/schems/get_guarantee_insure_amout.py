from pydantic.main import BaseModel


class GetGuaranteeInsureAmount(BaseModel):
    startGmtInsure: str
    endGmtInsure: str
    maxAge: int
    minAge: int
    maxSingleClaimAmount: str


class AmountSave(BaseModel):
    channel: int
    taskNo: str
    insurerId: int
    maxRate: str
    premiumRate: str
    premium: str
    insureCompanyId: int
    insuredCompanyId: int
    policyWeight: int
    insureMethod: int
    insureType: int
    directPay: int
    claimRules: list
    policyPays: list
    policyProcedures: list
    policyType: int
    sumClaimAmount: str
    maxFloat: str
    maxSingleClaimAmount: str
    gmtCreatedEnd: str
    startGmtInsure: str
    endGmtInsure: str
    maxAge: int
    minAge: int
    insuranceType: int
    drugType: int


class UserIn(BaseModel):
    username: list
    password: str
