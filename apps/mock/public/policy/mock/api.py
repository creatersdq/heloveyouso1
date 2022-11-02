import json
from datetime import datetime

from apps.extensions.xml_str_del import xml_to_json, json_to_xml
from apps.public.uuid_generate import random_no


class ApiBase(object):
    def __init__(self):
        a = 1

    def insure_data_del(
            self,
            request: any
    ) -> str:
        """
        保司投保mock接口数据处理
        :param request:接口入参
        :return:
        """

        request_json = json.loads(xml_to_json(request))
        # 保单号拼接- 标识+当前时间+随机整数
        policy_no = "AP" + str(datetime.now().strftime("%Y%m%d%H%M%S")) + random_no(10)
        water_no = request_json["RequestInfo"]["GeneralInfo"]["UUID"]
        sum_premium = request_json["RequestInfo"]["PolicyInfo"]["SumPremium"]
        sum_amount = request_json["RequestInfo"]["PolicyInfo"]["SumAmount"]
        start_date = request_json["RequestInfo"]["PolicyInfo"]["StartDate"] + " " + \
                     request_json["RequestInfo"]["PolicyInfo"][
                         "StartTime"]
        end_date = request_json["RequestInfo"]["PolicyInfo"]["EndDate"] + " " + \
                   request_json["RequestInfo"]["PolicyInfo"][
                       "EndTime"]

        # 定义返参
        data = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><ReturnInfo>    <GeneralInfoReturn>        
             <ErrorCode>00</ErrorCode>        <ErrorMessage>投保成功！</ErrorMessage>        
             <UUID>PN165778663813815902103375474364</UUID>    </GeneralInfoReturn>    <PolicyInfoReturn>        
             <DownloadUrl>http://pro-oss-baosi-partners.oss-cn-hangzhou.aliyuncs.com/ossEpolicyUrl/YPB/TB220811004.pdf</DownloadUrl>        <EndTime>2022-08-14 23:59:59</EndTime>        
             <PolicyNo>6803010110606220000344</PolicyNo>        <SaveMessage>投保成功！</SaveMessage>        
             <SaveResult>00</SaveResult>        <SaveTimes>2022-07-14 16:17:21</SaveTimes>        <StartTime>2022-05-15 
             00:00:00</StartTime>        <SumAmount>291000</SumAmount>        <SumPremium>29100</SumPremium>    
             </PolicyInfoReturn></ReturnInfo> """

        # 返参字段处理
        data_json = json.loads(xml_to_json(data))
        data_json["ReturnInfo"]["GeneralInfoReturn"]["UUID"] = water_no
        data_json["ReturnInfo"]["PolicyInfoReturn"]["SumPremium"] = sum_premium
        data_json["ReturnInfo"]["PolicyInfoReturn"]["SumAmount"] = sum_amount
        data_json["ReturnInfo"]["PolicyInfoReturn"]["StartTime"] = start_date
        data_json["ReturnInfo"]["PolicyInfoReturn"]["SaveTimes"] = end_date
        data_json["ReturnInfo"]["PolicyInfoReturn"]["EndTime"] = end_date
        data_json["ReturnInfo"]["PolicyInfoReturn"]["PolicyNo"] = policy_no
        data_xml = json_to_xml(data_json)
        return data_xml

    def claim_data_del(
            self,
            request: any
    ) -> str:
        """
        保司理赔mock接口数据处理
        :param request:接口入参
        :return:
        """
        # 入参处理
        request_json = json.loads(xml_to_json(request))
        # mock报案号拼接-标识+时间戳+随机整数
        regist_no = "AR" + str(datetime.now().strftime("%Y%m%d%H%M%S")) + random_no(4)
        water_no = request_json["RequestInfo"]["GeneralInfo"]["UUID"]

        # 返参处理
        data = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><ReturnInfo>  <GeneralInfoReturn>    
        <UUID>UG220711535153101525455515352212</UUID>    <ErrorCode>00</ErrorCode>  </GeneralInfoReturn>  
        <ClaimInfoReturn>    <SaveResult>00</SaveResult>    <SaveTimes>2022-07-11 14:04:56</SaveTimes>    <RegistVo>      
        <RegistNo>07803011060722000002</RegistNo>    </RegistVo>  </ClaimInfoReturn></ReturnInfo> """
        data_json = json.loads(xml_to_json(data))
        data_json["ReturnInfo"]["GeneralInfoReturn"]["UUID"] = water_no
        data_json["ReturnInfo"]["ClaimInfoReturn"]["RegistVo"]["RegistNo"] = regist_no
        data_json["ReturnInfo"]["ClaimInfoReturn"]["SaveTimes"] = str(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        data_xml = json_to_xml(data_json)
        return data_xml
