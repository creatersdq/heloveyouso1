import csv
from app.public.mock_chinese_name import RandomChineseName
from app.public.identity import IdNumber
import random
import hashlib
import requests
from app.extensions.random_number import StochasticNum
from app.extensions.logger import log
from app.curd.db_policy import call_back_policy_no, insurance_code_db, get_claim_data, get_insurance
from xml.dom.minidom import parseString


random_num = StochasticNum()


# 报销型太平csv投保文件
class CsvClass:
    def __init__(self, uuid: str):
        self.policy_rows = []
        self.claim_rows = []
        self.uuid = uuid
        self.headers = ["药联出单请求uuid", "投保码", "保额", "保费", "姓名", "身份证号", "手机号", "详细地址", "证件起期", "证件止期"]
        for i in range(200):
            # 投保码
            policy_num = StochasticNum.water_no("607468", 1)
            # 保额
            policy_lines = 4000
            # 保费
            policy_amount = 3200
            # 姓名
            chinese_name = RandomChineseName.random_name_str()
            # 身份证
            id_card_num = IdNumber.generate_id(random.randint(0, 1))
            # 手机号
            iphone_num = "18621010607"
            # 地址
            address = "境内"
            id_card_start = "2021/1/1"
            id_card_end = "9999/1/1"

            self.policy_rows.append(
                [self.uuid, policy_num, policy_lines, policy_amount, chinese_name, id_card_num, iphone_num, address,
                 id_card_start, id_card_end])
            insurance_code_db(uuid=uuid, name=chinese_name, id_card=id_card_num, insurance_code=policy_num)

    def taiping_bx(self):
        url = "http://opentest-backend.uniondrug.net/api/claim/upload"
        with open("/Users/living/PythonPrj/cn_ud_test_mock/app/public/zijin_policy/{}.csv".format(self.uuid), 'w',
                  encoding="GBK") as f:
            f_csv = csv.writer(f)
            f_csv.writerow(self.headers)
            f_csv.writerows(self.policy_rows)
        files = [
            ('files', ('{}.csv'.format(self.uuid),
                       open('/Users/living/PythonPrj/cn_ud_test_mock/app/public/zijin_policy/{}.csv'.format(self.uuid),
                            'rb'),
                       'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        ]
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        policy_file_address = response.json()['data']['url']
        return policy_file_address


def policy(uuid, file_address):
    """

    :param uuid:
    :param file_address:
    :return: 紫金投保
    """
    url = "https://test-open.zking.com/api/v1/insurance/nonAutoMobile/uniondrug/insureGroup"

    payload = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><RequestInfo><GeneralInfo><UUID></UUID><Md5Value></Md5Value></GeneralInfo><PolicyInfo><RiskCode>0656</RiskCode><RationType>YLJK-0656-BJ</RationType><KindList><Kind><KindCode></KindCode><Amount></Amount><Premium></Premium></Kind></KindList><BranchCode>2130000601</BranchCode><OperateTimes>2021-11-10 10:26:53</OperateTimes><StartDate>2021-10-31</StartDate><EndDate>2022-10-25</EndDate><StartTime>00:00:00</StartTime><EndTime>23:59:59</EndTime><SumAmount>800000</SumAmount><SumPremium>640000</SumPremium><LiabInfo><EquityNoQuantity>52</EquityNoQuantity></LiabInfo><Applicant><AppliName>上海聚音信息科技有限公司</AppliName><AppliIdNo>913101065820837146</AppliIdNo><AppliIdMobile>18621010607</AppliIdMobile><AppliAddress>上海市上海市上海市静安区江场路1401弄壹中心9号楼药联健康</AppliAddress><AppliIdentity>01</AppliIdentity></Applicant><Insured><InsuredName>上海聚音信息科技有限公司</InsuredName><InsuredIdNo>913101065820837146</InsuredIdNo><InsuredIdMobile>18621010607</InsuredIdMobile><InsuredAddress>上海市静安区江场路1401弄壹中心9号楼药联健康</InsuredAddress></Insured><ExtendInfos><ExtendInfo key="url"></ExtendInfo><ExtendInfo key="linkerName_T">王佳斐</ExtendInfo><ExtendInfo key="linkerMobile_T">18621010607</ExtendInfo><ExtendInfo key="linkerEmail_T">zoyulu@uniondrug.com</ExtendInfo></ExtendInfos></PolicyInfo></RequestInfo>"""
    headers = {
        'Content-Type': 'application/xml'
    }
    new_data = payload.replace("<UUID></UUID>", "<UUID>{}</UUID>".format(uuid))
    str = "{}".format(uuid) + "640000" + "UniondrugTest2020"
    hl = hashlib.md5()
    hl.update(str.encode(encoding="utf-8"))
    md_value = hl.hexdigest()
    new_new_data = new_data.replace("<Md5Value></Md5Value>", "<Md5Value>{}</Md5Value>".format(md_value))
    n_n_n_data = new_new_data.replace('<ExtendInfo key="url"></ExtendInfo>',
                                      '<ExtendInfo key="url">{}</ExtendInfo>'.format(file_address))
    response = requests.request("POST", url, headers=headers, data=n_n_n_data.encode("utf-8"))
    log.get_log("zijinPolicy", "INFO", "投保：" + n_n_n_data)
    log.get_log("zijinPolicy", "INFO", "接口返回：" + response.text)
    res_text = response.text
    doc = parseString(res_text)
    collection = doc.documentElement
    policy_no = collection.getElementsByTagName("PolicyNo")[0].childNodes[0].data
    call_back_policy_no(uuid=uuid, file_address=file_address, policy_no=policy_no)


class Claim:
    def __init__(self, uuid: str, policy_no: str):
        self.policy_no = policy_no
        self.uuid = uuid
        self.headers = ["投保码号", "投保码赔付金额", "连锁名称", "药品信息", "保单号", "消费时间", "姓名", "身份证号"]
        self.new_headers = ["投保码号", "投保码赔付金额", "连锁名称", "药品信息", "保单号", "报案号", "消费时间", "姓名", "身份证号"]
        self.data = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<RequestInfo>
  <GeneralInfo>
    <UUID></UUID>
    <Md5Value></Md5Value> 
  </GeneralInfo>
  <ClaimInfo>
    <BuscaseInfoVo>
          <PolicyNo></PolicyNo>
          <ReportorName>上海聚音</ReportorName>
          <ReportorNumber>18621010607</ReportorNumber>
    </BuscaseInfoVo>
    <MajorInfoVo>
          <DamageFlag>1</DamageFlag>
          <DamageTime>2021-11-08 14:05:15</DamageTime>
          <DamageAddress>上海市静安区江场路1401弄壹中心9号楼药联健康</DamageAddress>
          <DamageReasonCode>C00-C97</DamageReasonCode>
          <DamageReasonName>恶性肿瘤</DamageReasonName>
          <SumLoss>20000</SumLoss>
          <PayInfoVo>
              <AccountName>上海聚音信息科技有限公司</AccountName>
              <BankAccount>1001101719100022593</BankAccount>
              <OpenBankName>中国工商银行</OpenBankName>
              <BankCode>102100099996</BankCode>
              <OpenBankCode>102290010174</OpenBankCode>
              <OpenBankProvinceName>上海市</OpenBankProvinceName>
              <OpenBankCityName>上海市</OpenBankCityName>
              <OpenBankBranchName>中国工商银行股份有限公司上海市大连路支行</OpenBankBranchName>
         </PayInfoVo>
         <PayExtendVo>
             <PayCompanyVo>
                <CompanyName>上海聚音信息科技有限公司</CompanyName>
                <CompanyCode>2018090300000653697798</CompanyCode>
                <BusinessNumber>913101065820837146</BusinessNumber>
                <BusinessLicense>http://uniondrug-ota.oss-cn-shanghai.aliyuncs.com/outreach.equity.claim/1623917253/%E8%90%A5%E4%B8%9A%E6%89%A7%E7%85%A7%E4%BF%A1%E6%81%AF.jpg</BusinessLicense>
                <BusinessStartDate>2011-09-05</BusinessStartDate>
                <BusinessEndDate>2031-09-04</BusinessEndDate>
                <Address>上海市静安区江场路1401弄3号5层501</Address>
                <BusinessScope>从事信息、网络、计算机、电子科技领域内的技术开发、技术转让、技术咨询、技术服务，计算机软硬件、电子产品、办公设备的销售，电子商务(不得从事增值电信、金融业务)，电信业务，计算机系统集成，广告设计、制作、代理、发布，网络工程，市场信息咨询与调查(不得从事社会调查、社会调研、民意调查、民意测验)，会务服务，展览展示服务，市场营销策划，营养健康咨询服务，数据处理。【依法须经批准的项目，经相关部门批准后方可开展经营活动】</BusinessScope>
             </PayCompanyVo>
             <PayPersonVo>
                  <PayeeName>张潇臻</PayeeName>
                  <PayeeIdNo>320504197801264014</PayeeIdNo>
                  <PayeeIdNoUrl>http://uniondrug-ota.oss-cn-shanghai.aliyuncs.com/outreach.equity.claim/1623917220/%E6%AD%A3%E5%8F%8D%E9%9D%A2.jpg</PayeeIdNoUrl>
                  <PayeeIdNoStartDate>2017-10-24</PayeeIdNoStartDate>
                  <PayeeIdNoEndDate>2037-10-24</PayeeIdNoEndDate>
                  <Address>上海市浦东新区东绣路999弄2号1701室</Address>
             </PayPersonVo>
         </PayExtendVo>
    </MajorInfoVo>
    <ExtendInfos>
          <ExtendInfo key="url"></ExtendInfo>
    </ExtendInfos>
  </ClaimInfo>
</RequestInfo>
        """

    def file_address_rc(self, uuid):
        url = "http://opentest-backend.uniondrug.net/api/claim/upload"
        files = [
            ('files', ('{}.csv'.format(uuid),
                       open('/Users/living/PythonPrj/cn_ud_test_mock/app/public/zijin_claim/{}.csv'.format(uuid),
                            'rb'),
                       'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        ]
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        policy_file_address = response.json()['data']['url']
        return policy_file_address

    def claim_zijin(self):
        url = "http://221.226.62.39:9001/claim/ReceiveInfoServlet/YL/ClaimCase"
        headers = {
            'Content-Type': 'application/xml'
        }
        t = get_insurance(self.uuid)
        new_uuid = random_num.water_no("UG")
        claim_rows = []
        new_claim_rows = []
        for p in t:
            insurance_code = p[1]
            pay_amount = 100
            partner_name = "一心堂药业集团股份有限公司"
            drug_info = "西黄胶囊"
            policy_no = self.policy_no
            time = "2021-11-07 14:56:37"
            name = p[3]
            id_card = p[2]
            claim_rows.append([insurance_code, pay_amount, partner_name, drug_info, policy_no, time, name, id_card])
            with open("/Users/living/PythonPrj/cn_ud_test_mock/app/public/zijin_claim/{}.csv".format(new_uuid), 'w',
                      encoding="GBK") as f:
                f_csv = csv.writer(f)
                f_csv.writerow(self.headers)
                f_csv.writerows(claim_rows)
        file_address = self.file_address_rc(new_uuid)
        n_data = self.data.replace("<PolicyNo></PolicyNo>", "<PolicyNo>{}</PolicyNo>".format(self.policy_no))
        str = new_uuid + "20000" + "UniondrugTest2020"
        hl = hashlib.md5()
        hl.update(str.encode(encoding="utf-8"))
        md_value = hl.hexdigest()
        n_n_data = n_data.replace("<Md5Value></Md5Value>", "<Md5Value>{}</Md5Value>".format(md_value))
        nn_data = n_n_data.replace("<UUID></UUID>", "<UUID>{}</UUID>".format(new_uuid))
        nn_n_data = nn_data.replace('<ExtendInfo key="url"></ExtendInfo>',
                                    '<ExtendInfo key="url">{}</ExtendInfo>'.format(file_address))
        print("接口请求")
        re = requests.post(url=url, headers=headers, data=nn_n_data.encode("utf-8"))
        log.get_log("zijinClaim", "INFO", "投保：" + nn_n_data)
        log.get_log("zijinClaim", "INFO", "接口返回：" + re.text)
        doc = parseString(re.text)
        collection = doc.documentElement
        regist_no = collection.getElementsByTagName("RegistNo")[0].childNodes[0].data
        print("数据预处理")
        for pp in t:
            # print("xxxxxxxx")
            insurance_code = pp[1]
            pay_amount = 100
            partner_name = "一心堂药业集团股份有限公司"
            drug_info = "西黄胶囊"
            policy_no = self.policy_no
            time = "2021-11-07 14:56:37"
            name = pp[3]
            id_card = pp[2]
            new_claim_rows.append(
                [insurance_code, pay_amount, partner_name, drug_info, policy_no, regist_no, time, name, id_card])
            with open("/Users/living/PythonPrj/cn_ud_test_mock/app/public/zijin_claim/{}.csv".format(new_uuid), 'w',
                      encoding="GBK") as f:
                f_csv = csv.writer(f)
                f_csv.writerow(self.new_headers)
                f_csv.writerows(new_claim_rows)
        file_address = self.file_address_rc(new_uuid)
        print(file_address)
        # print(nn_n_data)


if __name__ == '__main__':
    # for i in range(50):
    #     uuid = random_num.water_no("PN")
    #     tt = CsvClass(uuid)
    #     file_address = tt.taiping_bx()
    #     policy(uuid, file_address)

    # claim = Claim("PN2021111211z08", "20656213000021000156")
    # claim.claim_zijin()
    c = get_claim_data()
    for i in c:
        uuid = i[1]
        policy_no = i[2]
        claim = Claim(uuid, policy_no)
        claim.claim_zijin()

