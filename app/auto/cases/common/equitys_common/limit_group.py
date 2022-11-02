def dic_data():
    limit_list = []
    amount = [{"isUnlimitedAmount": "2", "limitAmountType": "1", "limitAmount": "25"},
              {"isUnlimitedAmount": "1", "limitAmountType": "4", "limitAmount": "25"},
              {"isUnlimitedAmount": "1", "limitAmountType": "3", "limitAmount": "25"},
              {"isUnlimitedAmount": "1", "limitAmountType": "2", "limitAmount": "25"},
              {"isUnlimitedAmount": "1", "limitAmountType": "1", "limitAmount": "25"}]
    money = [{"isUnlimitedMoney": "2", "limitMoneyType": "1", "limitMoney": "2500"},
             {"isUnlimitedMoney": "1", "limitMoneyType": "4", "limitMoney": "2500"},
             {"isUnlimitedMoney": "1", "limitMoneyType": "3", "limitMoney": "2500"},
             {"isUnlimitedMoney": "1", "limitMoneyType": "2", "limitMoney": "2500"},
             {"isUnlimitedMoney": "1", "limitMoneyType": "1", "limitMoney": "2500"}]

    for i in range(len(amount)):
        for j in range(len(money)):
            d = {}
            d.update(amount[i])
            d.update(money[j])
            limit_list.append(d)
            # print(dic)

    return limit_list


# import json
# print(json.dumps(dic_data()))