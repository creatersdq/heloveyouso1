import json
import xmltodict


def xml_to_json(xml_str: str) -> str:
    """
    xml字符串转json字符串
    :param xml_str:
    :return:
    """
    # parse是的xml解析器
    xml_parse = xmltodict.parse(xml_str)
    # json库dumps()是将dict转化成json格式，loads()是将json转化成dict格式。
    # dumps()方法的ident=1，格式化json
    json_str = json.dumps(xml_parse, indent=1)
    return json_str


def json_to_xml(json_str: str) -> str:
    """
    json字符串转xml字符串
    :param json_str:
    :return:
    """
    # xmltodict库的unparse()json转xml
    xml_str = xmltodict.unparse(json_str)
    return xml_str


if __name__ == "__main__":
    xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><ReturnInfo>    <GeneralInfoReturn>        
    <ErrorCode>00</ErrorCode>        <ErrorMessage>投保成功！</ErrorMessage>        
    <UUID>PN165778663813815902103375474364</UUID>    </GeneralInfoReturn>    <PolicyInfoReturn>        
    <DownloadUrl>1</DownloadUrl>        <EndTime>2022-08-14 23:59:59</EndTime>        
    <PolicyNo>6803010110606220000344</PolicyNo>        <SaveMessage>投保成功！</SaveMessage>        
    <SaveResult>00</SaveResult>        <SaveTimes>2022-07-14 16:17:21</SaveTimes>        <StartTime>2022-05-15 
    00:00:00</StartTime>        <SumAmount>291000</SumAmount>        <SumPremium>29100</SumPremium>    
    </PolicyInfoReturn></ReturnInfo> """

    a = xml_to_json(xml)  # 调用转换函数
    print(a)
    print(type(a))
    c = json.loads(a)
    c["RequestInfo"]["ClaimInfo"]["MajorInfoVo"]["SumLoss"] = "2000"
    b = json_to_xml(c)
    print(b)
    print(type(b))
