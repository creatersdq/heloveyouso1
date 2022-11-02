import copy
import datetime
import json
import random

import requests
import asyncio

from apps.models.policy.insure import ClaimPayInfo
from apps.public.policy_async import fetch_async
from apps.curd.policy.crud_finance import order_reset, get_pool_claim
from apps.curd.policy.crud_insure import get_policy_object, get_claim_records, get_batch_no, insert_claim_pay_info
from apps.public.uuid_generate import random_no
from apps.extensions.logger import log
from apps.schems.policy.mock import OrderDetail
from apps.public.policy.policy_base import PolicyBase


class Ypb(PolicyBase):
    """
    药品保-投保理赔数据mock
    """

    def __init__(self, dev: str):
        super(Ypb, self).__init__(dev)
        self.mock_claim_no_data = []
        self.mock_order_attachments_data = []
        self.mock_claim_records_data = None
        # 异步json队列
        self.tasks = []
        # 信号量
        self.sem = asyncio.Semaphore(50)

    def mock_pool_claim(
            self,
            order_detail: OrderDetail
    ) -> any:
        """
        释放资金池订单
        :return:
        """
        try:
            log.get_log(
                "policy_data_mock",
                "INFO",
                "----------实时释放资金池订单开始----------\n计算资金池订单更新日期，向前追溯期：{}".format(
                    order_detail.retrospectNum
                )
            )
            # 根据追溯期计算更新日期
            update_time = (
                    datetime.datetime.now() + datetime.timedelta(days=order_detail.retrospectNum)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            log.get_log(
                "policy_data_mock",
                "INFO",
                "资金池订单更新日期:{}".format(update_time)
            )
            # 数据更新字段处理
            update_data = self.data_pool_claim
            update_data["gmt_updated"] = update_time
            update_data["gmt_paid"] = update_time
            update_data["gmt_created"] = update_time
            update_data["direct_pay"] = order_detail.directPay
            update_data["drug_type"] = order_detail.drugType
            update_data["medical_deviced"] = order_detail.medicalDeviced
            update_data["special_diseased"] = order_detail.specialDiseased
            update_data["special_disease_type"] = order_detail.specialDiseaseType
            update_data["insure_group_id"] = order_detail.insureGroupId
            update_data["claim_amount"] = order_detail.sumClaim
            # 更新数据库
            if order_detail.gear == 0:
                # 非档位制度批量update
                order_reset(
                    pool_id_list=self.pool_id_list,
                    update_data=update_data,
                    dev=self.dev
                )
                log.get_log(
                    "policy_data_mock",
                    "INFO",
                    "资金池订单id:{}\n更新数据:{}".format(self.pool_id_list, update_data)
                )
            elif order_detail.gear != 0:
                # 获取资金池订单list
                pool_list = get_pool_claim(
                    pool_id=self.pool_id_list,
                    dev=self.dev
                )
                # 计算订单数
                list_num = len(pool_list)
                # 分配订单金额保存至ii列表
                sum = 0
                ii = []
                if list_num:
                    for i in range(list_num):
                        # 非最后一个值
                        if i != list_num - 1:
                            # 随机数（1，档位金额）
                            dd = random.randint(1, order_detail.gear)
                            # 添加至list
                            ii.append(dd)
                            # 已分配金额汇总
                            sum += dd
                        # 最后一个值
                        elif i == list_num - 1:
                            # 总金额-已分配金额
                            dd = order_detail.gear * list_num - sum
                            ii.append(dd)
                            break
                # 根据金额依次更新数据库
                uu = 0
                for u in ii:
                    # 获取id
                    pool_id = [pool_list[uu].id]
                    print(pool_id)
                    # 获取金额
                    update_data["claim_amount"] = u
                    # 更新数据库
                    order_reset(
                        pool_id_list=pool_id,
                        update_data=update_data,
                        dev=self.dev
                    )
                    log.get_log(
                        "policy_data_mock",
                        "INFO",
                        "档位制更新订单-订单id{},更新数据{}".format(pool_id, update_data)
                    )
                    uu += 1
            log.get_log(
                "policy_data_mock",
                "INFO",
                "----------实时释放药品保资金池订单结束----------"
            )
        except Exception as e:
            log.get_log(
                "policy_data_mock",
                "ERROR",
                "实时释放资金池订单失败:{}".format(e)
            )

    def get_pool_amount(
            self,
            order_detail: OrderDetail
    ) -> dict:
        """
        查询资金池
        :return:
        """
        try:
            # 根据追溯器计算选单起期&止期
            start_date = str(datetime.date.today() + datetime.timedelta(order_detail.retrospectNum))
            end_date = str(datetime.date.today() + datetime.timedelta(-1))
            log.get_log(
                "policy_data_mock",
                "INFO",
                "根据追溯器计算选单起期&止期，向前追溯期：{},计算选单起期:{}，计算选单止期:{}".format(
                    order_detail.retrospectNum,
                    start_date,
                    end_date
                )
            )

            # 入参处理
            self.data_get_pool_amount["startDate"] = start_date
            self.data_get_pool_amount["endDate"] = end_date
            self.data_get_pool_amount["directPay"] = order_detail.directPay
            self.data_get_pool_amount["drugType"] = order_detail.drugType
            self.data_get_pool_amount["insureCompanyId"] = order_detail.insureGroupId
            self.data_get_pool_amount["latitude"] = order_detail.latitude
            self.data_get_pool_amount["medicalDeviced"] = order_detail.medicalDeviced

            # 查询资金池请求入参
            request_body = json.dumps(self.data_get_pool_amount)
            log.get_log(
                "policy_data_mock",
                "INFO",
                "查询资金池请求入参:{}".format(json.loads(request_body))
            )

            # 实时查询资金池可投金额
            response_body = requests.post(
                self.jm_domain + self.api_get_pool_amount,
                data=request_body,
                headers=self.request_header
            ).json()
            log.get_log(
                "policy_data_mock",
                "INFO",
                "查询资金池响应报文:{}\n----------实时查询资金池金额结束----------".format(response_body)
            )
            return response_body
        except Exception as e:
            log.get_log(
                "policy_data_mock",
                "ERROR",
                "实时查询资金池金额失败:{}".format(e)
            )

    def mock_claim_data(
            self,
            policy_no: str
    ) -> any:
        """
        理赔数据mock
        :param policy_no:
        :return:
        """
        try:
            log.get_log(
                "policy_data_mock",
                "INFO",
                "----------理赔数据推送开始----------"
            )
            # 随机生成billNo、damageNo、orderNo
            bill_no_base = "MOCK"
            damage_no_base = "MOCK"
            a = ''
            b = ''
            now_time = str(datetime.datetime.now().strftime('%Y-%m-%d')).replace("-", "")
            # 字符拼接：当天日期+随机整数
            bill_no = bill_no_base + now_time + random_no(20)
            damage_no = damage_no_base + now_time + random_no(18)
            order_no = now_time + random_no(11)
            # 获取投保标
            policy_object_list = get_policy_object(policy_no=policy_no, dev=self.dev)
            log.get_log(
                "policy_data_mock",
                "INFO",
                "获取投保标:{}".format(policy_object_list)
            )

            # 根据投保标依次推送理赔数据
            log.get_log(
                "policy_data_mock",
                "INFO",
                "开始推送理赔数据billNo:{}".format(bill_no)
            )
            n = 0
            for i in policy_object_list:
                # damageNo、orderNo处理
                damage_no_del = damage_no + str(n + 1)
                order_no_del = order_no + str(n + 1)
                no_list = {"billNo": bill_no, "damageNo": damage_no_del, "orderNo": order_no_del}
                self.mock_claim_no_data.append(no_list)
                log.get_log(
                    "policy_data_mock",
                    "INFO",
                    "理赔数据处理:{}".format(no_list)
                )
                # 理赔推送入参处理
                self.data_claim["majorList"][0]["userInfo"]["orderNo"] = no_list["orderNo"]
                self.data_claim["majorList"][0]["damageNo"] = no_list["damageNo"]
                self.data_claim["policyNo"] = policy_no
                self.data_claim["billNo"] = bill_no
                self.data_claim["majorList"][0]["userInfo"]["userName"] = i.insuredName
                self.data_claim["majorList"][0]["userInfo"]["certificateNo"] = i.insuredIdNo
                self.data_claim["majorList"][0]["userInfo"]["equityNo"] = i.equityNo
                self.data_claim["majorList"][0]["userInfo"]["equityConsumeTime"] = str(datetime.datetime.now())
                self.data_claim["majorList"][0]["damageTime"] = str(datetime.datetime.now())
                self.data_claim["majorList"][0]["lossList"]["sumClaim"] = 100
                # self.data_claim["majorList"][0]["userInfo"]["partnerCode"] = ''
                # self.data_claim["majorList"][0]["userInfo"]["partnerName"] = ''

                # url
                url = self.module_domain + self.api_claim
                # 入参
                request_body = json.dumps(self.data_claim)

                # 推送理赔数据
                response_body = requests.post(url=url, data=request_body,
                                              headers=self.request_header).json()
                log.get_log(
                    "policy_data_mock",
                    "INFO",
                    "理赔数据推送-请求地址:{}，入参{}，返参{}".format(
                        url,
                        request_body,
                        response_body
                    )
                )
                n += 1
            log.get_log(
                "policy_data_mock",
                "INFO",
                "----------理赔数据推送结束----------"
            )
            # 获取理赔记录
            batch_id = get_batch_no(bill_no, self.dev)
            self.mock_claim_records_data = get_claim_records(batch_id, self.dev)
        except Exception as e:
            log.get_log(
                "policy_data_mock",
                "ERROR",
                "理赔数据推送失败:{}".format(e)
            )

    def invoice_data_mock(
            self,
            bill_no=None
    ) -> any:
        """
        发票数据mock
        :param
        :return:
        """
        try:
            # 若传入bill_no,则以传入参数为准
            if bill_no is not None:
                batch_id = get_batch_no(
                    bill_no,
                    self.dev
                )
                self.mock_claim_records_data = get_claim_records(
                    batch_id,
                    self.dev
                )

            log.get_log(
                "policy_data_mock",
                "INFO",
                "----------发票数据推送开始billNo:{}----------".format(
                    self.mock_claim_records_data[0].billNo
                )
            )

            # 计算批次开票总金额
            sum_damage_amount = 0
            for i in self.mock_claim_records_data:
                sum_damage_amount += i.damageAmount
            # 发票数据处理
            self.data_invoice["uuid"] = random_no(32)
            self.data_invoice["waterNo"] = random_no(14)
            self.data_invoice["invoiceInfos"][0]["invoiceCode"] = random_no(10)
            self.data_invoice["invoiceInfos"][0]["invoiceNo"] = random_no(8)
            self.data_invoice["invoiceInfos"][0]["partnerCode"] = self.mock_claim_records_data[0].partnerCode
            self.data_invoice["invoiceInfos"][0]["invoiceCompany"] = self.mock_claim_records_data[0].partnerName
            self.data_invoice["invoiceInfos"][0]["policyNo"] = self.mock_claim_records_data[0].policyNo
            self.data_invoice["policyNo"] = self.mock_claim_records_data[0].policyNo
            self.data_invoice["invoiceInfos"][0]["invoiceDate"] = str(self.mock_claim_records_data[0].gmtCreated)
            self.data_invoice["invoiceInfos"][0]["billNo"] = self.mock_claim_records_data[0].billNo
            self.data_invoice["invoiceInfos"][0]["taxSumAmount"] = sum_damage_amount * 0.13
            self.data_invoice["invoiceInfos"][0]["invoiceSumAmount"] = sum_damage_amount
            self.data_invoice["invoiceInfos"][0]["taxPointInfos"][0]["invoiceAmount"] = sum_damage_amount
            self.data_invoice["invoiceInfos"][0]["taxPointInfos"][0]["taxAmount"] = sum_damage_amount * 0.13
            self.data_invoice["invoiceInfos"][0]["billPartnerAmount"] = sum_damage_amount

            # 发票推送接口入参
            request_body = json.dumps(self.data_invoice)
            # 发票数据推送
            response_body = requests.post(
                self.module_domain + self.api_invoice_register,
                data=request_body,
                headers=self.request_header
            ).json()
            log.get_log(
                "policy_data_mock",
                "INFO",
                "发票数据推送-请求地址:{},入参:{},返参:{}\n----------发票数据推送结束----------".format(
                    self.module_domain + self.api_invoice_register,
                    request_body,
                    response_body
                )
            )
        except Exception as e:
            log.get_log(
                "policy_data_mock",
                "ERROR",
                "发票数据推送失败:{}".format(e)
            )

    async def order_attachments_mock(
            self,
            session,
            bill_no=None
    ) -> any:
        """
        订单影像件数据mock
        :return:
        """
        try:
            # 若传入bill_no, 则以传入参数为准
            if bill_no is not None:
                batch_id = get_batch_no(bill_no, self.dev)
                self.mock_claim_records_data = get_claim_records(
                    batch_id=batch_id,
                    dev=self.dev
                )
            log.get_log(
                "policy_data_mock",
                "INFO",
                "----------订单影像件推送开始----------"
            )
            # 订单影像件推送接口
            url = self.module_domain + self.api_order_attachments
            order_num = 1
            for i in self.mock_claim_records_data:
                # 获取orderNo
                order_no = i.orderNo
                # 获取影像件信息
                log.get_log(
                    "policy_data_mock",
                    "INFO",
                    "订单影像件数据处理-orderNo:{}".format(order_no)
                )
                # 订单影像件数据处理
                self.data_order_attachments["orderNo"] = order_no
                self.data_order_attachments["userName"] = i.userName
                self.data_order_attachments["idcardNo"] = i.certificateNo
                self.data_order_attachments["partnerName"] = i.partnerName
                self.data_order_attachments["partnerCode"] = i.partnerName
                self.data_order_attachments["storeName"] = i.partnerName
                # 影像件url处理
                attachments_url_1 = {
                    "fileType": 1,
                    "fileUrl": self.attachments_1[order_num]
                }
                attachments_url_2 = {
                    "fileType": 2,
                    "fileUrl": self.attachments_2[order_num]
                }
                attachments_url_3 = {
                    "fileType": 3,
                    "fileUrl": self.attachments_3[order_num]
                }
                attachments_url_4 = {
                    "fileType": 4,
                    "fileUrl": self.attachments_4[order_num]
                }
                attachments_url_list = [
                    attachments_url_1,
                    attachments_url_2,
                    attachments_url_3,
                    attachments_url_4
                ]
                self.data_order_attachments["attachments"] = attachments_url_list
                attachments_info = {
                    "orderNo": order_no,
                    "attachmentsList": attachments_url_list
                }
                # 深拷贝,解决可变类型赋值问题（body指向一个新的内存地址）
                body = copy.deepcopy(self.data_order_attachments)
                # 插入异步json队列
                task = asyncio.create_task(fetch_async(
                    body,
                    url,
                    session
                ))
                self.tasks.append(task)
                self.mock_order_attachments_data.append(attachments_info)
                order_num += 1
                log.get_log(
                    "policy_data_mock",
                    "INFO",
                    "tasks:{}".format(self.tasks)
                )
            # 执行coroutine
            await asyncio.gather(*self.tasks)
            log.get_log(
                "policy_data_mock",
                "INFO",
                "----------订单影像件推送结束----------"
            )
        except Exception as e:
            log.get_log(
                "policy_data_mock",
                "ERROR",
                "订单影像件推送失败:{}".format(e)
            )

    def claim_pay_info_mock(self) -> any:
        """
        反洗钱信息数据mock
        :return:
        """
        claim_data = self.mock_claim_records_data[0]
        insert_list = []
        insert_data = ClaimPayInfo(
            batchId=claim_data.batchId,
            partnerCode=claim_data.partnerCode,
            acctName=claim_data.partnerName,
            acctNo="866160100190053321",
            acctBankName="招商银行股份有限公司",
            acctBranchName="招商银行股份有限公司上海金山支行",
            acctBranchNode="308290003896",
            provinceName="上海市",
            provinceCode="310000",
            cityName="上海市",
            cityCode="310100",
            businessScope="许可项目：药品零售；第三类医疗器械经营；",
            businessEndDate="长期",
            businessStartDate="2020-05-01",
            businessAddress="江苏省南京市雨花台区金证科技园18栋",
            businessNumber="RX1234567654R12242",
            partnerName=claim_data.partnerName,
            payeeIdNoEndDate="长期",
            payeeIdNoStartDate="2014-07-17",
            payeeIdNoUrl="http://rc-oss-baosi-partners.oss-cn-hangzhou.aliyuncs.com/outreach.equity.claim/1653284872/mergeImage/220523565749979997555756565973.jpg",
            payeeName="冯海波",
            payeeIdNo="441882198610166014",
            payeeMobile="13857660044",
            payeeAddress="广东省佛山市禅城区南庄 镇紫洞南路96号1区29座202房",
            businessLicense="http://uniondrug.oss-cn-hangzhou.aliyuncs.com/backend.merchant/l0lfs7rqup3qghmfqlo2foqbbv.jpg",
            payeeIdNoFront="http://uniondrug.oss-cn-hangzhou.aliyuncs.com/backend.merchant/06fn69bccklc6gm9g15nlp1pbe.png",
            payeeIdNoBack="http://uniondrug.oss-cn-hangzhou.aliyuncs.com/backend.merchant/o9c60a68kohet94vfvdcsm6aoc.png"
        )
        insert_list.append(insert_data)
        insert_claim_pay_info(
            dev=self.dev,
            insert_data=insert_list
        )


if __name__ == "__main__":
    # p = PolicyBase()
    p = Ypb(dev="test")
    # print(p.dev)
    p.mock_claim_data(policy_no='6390080101820220000230')
    p.claim_pay_info_mock()
    # p.invoice_data_mock()
    # p.order_attachments_mock('TN202207254474151824362722468880')
    # p.order_attachments_mock()
    # p.order_attachments_mock()
    # p.mock_claim_no_data["bill_no"] = "TN202207047605122595215686193629"
    # p.order_attachments_mock()
    # p = PolicyBase("RC")
    # print(p.response, p.request)
    # p.invoice_data_mock()
    # class C(object):
    #     x = 4
    # c = C()
    # c.y = 5
    # print(c.__dict__)
    # ddd = {}
    # data = json.dumps(c, default=lambda a: a.__dict__)
    # print(data)
    # output --> {'y': 5}
