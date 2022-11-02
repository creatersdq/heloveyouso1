import time
from datetime import datetime

from app.curd.policy.crud_insure import insert_db_data
from app.models.policy.insure import ClaimSubRecords, PaymentRecords
from app.extensions.logger import log


def data_base(num: int, dev: str) -> any:
    """
    赔案流水表批量新增数据
    :param num:
    :param dev:
    :return:
    """

    n = 1
    res = []
    now_time = datetime.now()
    # 生成list
    for i in range(num):
        a = int(time.time())
        b = str(a) + str(n)
        n += 1
        res.append(b)

    insert_list_claim = []
    insert_list_pay = []
    if dev == 'test':
        for u in res:
            data = ClaimSubRecords(
                batchId=288191,
                waterNo=u,
                registNo=u,
                policyNo="2049101002022300004",
                systemCode="PropertyInsuranceDrug",
                partnerCode="20",
                totalNum=1,
                totalAmount=7.92,
                sumClaim=7.92,
                sumClaimed=0,
                sumClaimPaid=0,
                claimTime='2022-08-03 15:20:40',
                status='07',
                gmtCreated=now_time
            )
            insert_list_claim.append(data)

        for j in res:
            data = PaymentRecords(
                refNo=j,
                tradeAmount=7.92,
                tradeDate='2022-08-03',
                tradeTime='2022-08-03 15:01:41',
                ugAcctNo='1001101719100022593',
                acctName='长江财险',
                acctNo='121907664910802',
                acctBankNode='308290003263',
                acctBankName='招商银行上海分行民生支行',
                acctType='C',
                feeType=1,
                status=0,
                comment=j,
                gmtCreated=now_time
            )
            insert_list_pay.append(data)

    elif dev == "rc":
        for uu in res:
            data = ClaimSubRecords(
                batchId=28840,
                waterNo=uu,
                registNo=uu,
                policyNo="6390080101820220000245",
                systemCode="UniondrugSynGroupV3_0",
                partnerCode="2018090300063453697303",
                totalNum=1,
                totalAmount=7.92,
                sumClaim=7.92,
                sumClaimed=0,
                sumClaimPaid=0,
                claimTime='2022-08-04 15:20:40',
                status='07',
                gmtCreated=now_time
            )
            insert_list_claim.append(data)

        for jj in res:
            data = PaymentRecords(
                refNo=jj,
                tradeAmount=7.92,
                tradeDate='2022-08-04',
                tradeTime='2022-08-04 15:01:41',
                ugAcctNo='1001101719100022593',
                acctName='长江财险',
                acctNo='121907664910802',
                acctBankNode='308290003263',
                acctBankName='招商银行上海分行民生支行',
                acctType='C',
                feeType=1,
                status=0,
                comment=jj,
                gmtCreated=now_time
            )
            insert_list_pay.append(data)

    try:
        insert_db_data(dev=dev, insert_data=insert_list_claim)
        log.get_log(
            "info",
            "INFO",
            "insert_list_claim执行完成:{},环境:{}".format(datetime.now(), dev)
        )
        insert_db_data(dev=dev, insert_data=insert_list_pay)
        log.get_log(
            "info",
            "INFO",
            "insert_list_pay执行完成:{}:{}".format(datetime.now(), dev)
        )
    except Exception as e:
        log.get_log(
            "info",
            "ERROR",
            "执行失败:{}".format(e)
        )


if __name__ == "__main__":
    data_base(dev="test", num=1)
