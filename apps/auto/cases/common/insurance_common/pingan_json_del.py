import json
from apps.db_actions.insurance_actions.insure_db_actions import get_object

# 平安北分-生成批量投保人
control1 = '{"partnerName":"P_YLJK_PE","departmentCode":"20103","applicantInfo":{"name":"上海聚音信息科技有限公司",' \
           '"certificateType":"01","certificateNo":"231202199205182038","mobileTelephone":"13530338981",' \
           '"personnelType":"0"},"productInfoList":[{"baseInfo":{"insuranceBeginDate":"2022-05-07 00:00:00",' \
           '"insuranceEndDate":"2023-05-06 23:59:59","productCode":"MP03000695","transactionNo":"1252342300013498",' \
           '"totalActualPremium":130},"specialPromiseList":[{"promiseCode":"TP030000520000005","promiseDesc":"efwef",' \
           '"promiseType":"Y"}],"riskGroupInfoList":[{"applyNum":1,"productPackageType":"PK00029108",' \
           '"riskPersonInfoList": '
riskGroupInfoList = ''
control2 = '}]}]}'
my_dict = {"certificateNo": "320802197412142025", "certificateType": "01", "name": "刘冬梅",
           "relationshipWithApplicant": "1", "totalActualPremium": 13}
# loop to emulate your data structure
c = ''
count = 1
# start_id = 5139806
# start_id = 5139786
start_id = 5139766
while count <= 10:
    # 身份证号码/身份证名称value替换
    my_dict["certificateNo"] = get_object(start_id).insuredIdNo
    my_dict["name"] = get_object(start_id).insuredName
    # print(my_dict)
    # 字典转json
    j = json.dumps(my_dict, ensure_ascii=False)
    # print(type(j))
    # json转字典
    # l = json.loads(j)
    # print(type(l))
    if count == 10:
        c = c + j
    else:
        c = c + j + ","
    count = count + 1
    start_id = start_id - 1

riskGroupInfoList = '[' + c + ']'
# print("处理结果"+riskGroupInfoList)
# 拼接参数
control = control1 + riskGroupInfoList + control2
# 写入json文件
json.dump(control, open('configuration.json', 'w', encoding="utf-8"), indent=4)
print(control)
# json.dump(data,open('configuration.json', 'w'),indent=4)
