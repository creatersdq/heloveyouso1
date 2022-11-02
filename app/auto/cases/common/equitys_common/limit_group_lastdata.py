from apps.cases.common.equitys_common.limit_group import dic_data

a = dic_data()

"""
样式
list_a = [
    ["策略：单用户领取数量 次数无限制 每日 0次 金额无限制 每月 800", {
        "isUnlimitedAmount": "2",
        "limitAmountType": "4",
        "limitAmount": "0",
        "isUnlimitedMoney": "2",
        "limitMoneyType": "3",
        "limitMoney": "800"
    }]
]
"""

isUnlimitedAmountDict = {"2": "次数无限制,", "1": "次数有限制,"}
isUnlimitedMoneyDict = {"2": ",金额无限制,", "1": ",金额有限制,"}
limitAmountTypeDict = {"1": "终身次数:", "2": "每年:", "3": "每月:", "4": "每日:"}
limitMoneyTypeDict = {"1": "终身金额:", "2": "每年:", "3": "每月:", "4": "每日:"}

def last_data():
    list_last = []
    for i in a:
        list_i = []
        empty_list = ["策略:单用户领取数量:"]

        for k in i.keys():
            # 终身次数限制
            if k == "isUnlimitedAmount":
                empty_list.append(isUnlimitedAmountDict[i[k]])
                # print("{}".format(isUnlimitedAmountDict[i[k]]))
            # 次数年月日
            elif k == "limitAmountType":
                empty_list.append(limitAmountTypeDict[i[k]])
                # print("{}".format(limitAmountTypeDict[i[k]]))
            # 具体次数
            elif k == "limitAmount":
                empty_list.append(i[k])
                # print("{}".format(i[k]))
            # 终身金额限制
            elif k == "isUnlimitedMoney":
                empty_list.append(isUnlimitedMoneyDict[i[k]])
                # print("{}".format(isUnlimitedMoneyDict[i[k]]))
            # 金额终身
            elif k == "limitMoneyType":
                empty_list.append(limitMoneyTypeDict[i[k]])
                # print("{}".format(limitMoneyTypeDict[i[k]]))
            # 具体终身
            elif k == "limitMoney":
                empty_list.append(i[k])
                # print("{}".format(i[k]))
        x = "".join(empty_list)
        list_i.append(x)
        list_i.append(i)
        list_last.append(list_i)

    return list_last


# list_last = last_data()
# print(list_last)



