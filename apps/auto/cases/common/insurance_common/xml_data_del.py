from xml.dom import minidom
from apps.extensions.logger import log


def xml_analysis(xml_str, nodes_key, object_key):
    """
    XML报文解析
    :param: xml_str : xml字符串
    :param: nodes_key : 一层key
    :param: object_key : 二层key
    :return: 二层value
    """
    try:
        # 解析xml字符串
        doc = minidom.parseString(xml_str)
        # 实例化
        root = doc.documentElement
        # 获取xml节点对象集合
        nodes = root.getElementsByTagName(nodes_key)[0]
        # 获取xml节点对象的具体信息
        element = nodes.getElementsByTagName(object_key)[0]
        # 获得文本值
        data = element.childNodes[0].data
        return data
    except Exception as e:
        log.get_log("insurance_interconnection", "INFO",
                    "xml字符串解析失败:{},key1:{},key2:{}".format(e, nodes_key, object_key))
        return None


if __name__ == "__main__":
    n = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<ReturnInfo>\n    <GeneralInfoReturn>\n       " \
        " <UUID>PN165880043372162720836090998641</UUID>\n        <ErrorCode>00</ErrorCode>\n        " \
        "<ErrorMessage>\u8f6c\u4fdd\u6210\u529f</ErrorMessage>\n    </GeneralInfoReturn>\n    <PolicyInfoReturn>\n    " \
        "    <PolicyNo>6390080101820220000243</PolicyNo>\n        <SumAmount>13333.4</SumAmount>\n        " \
        "<SumPremium>4000.02</SumPremium>\n        <PolicyUrl>http://www.chgic.com/webquery/</PolicyUrl>\n        " \
        "<SaveResult>00</SaveResult>\n        <SaveMessage>\u8f6c\u4fdd\u6210\u529f</SaveMessage>\n        " \
        "<SaveTimes>2022-07-26T09:55:42.720+08:00</SaveTimes>\n    </PolicyInfoReturn>\n</ReturnInfo>\n "
    a = xml_analysis(n, "PolicyInfoReturn", "PolicyNo")
    print(a)
