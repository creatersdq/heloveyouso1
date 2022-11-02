import time
from apps.db_actions.itude_actions.partners import get_partner_common, get_store_partner, get_goods_partner, \
    get_total_goods
import requests


def count_partner():
    # 统计接入连锁数
    count_partner = get_partner_common("1")
    count_partner = count_partner[0][0]
    return count_partner


def count_goods_store(partner_id=None):
    #  统计接入商品数和门店数
    count_goods = get_total_goods(3, partner_id)
    count_stores = get_total_goods(22, partner_id)
    count_goods = ("接入商品数：", count_goods[0][0])
    count_stores = ("接入门店数：", count_stores[0][0])
    return count_goods, count_stores


def total_quality_score():
    # 获取所有连锁的cooperation
    # cooperation_data = get_partner_common("2")
    # cooperation_list = list(map(lambda x: x[0], cooperation_data))

    score_list = []
    score_list1 = []
    score_list2 = []

    for i in range(3):
        if i == 0:
            url = "http://outreach-partners-rating-api.turboradio.cn/export"
            resp = requests.get(url)
            res = resp.json()
            if res["errno"] == "0":
                for i in res["data"][0]:
                    dict = {}
                    dict["common_name"] = i["common_name"]
                    dict["result_score"] = i["result_score"]
                    score_list.append(dict)
            else:
                print("接口错误")

        if i == 1:
            url = "http://outreach-partners-rating-api.turboradio.cn/export"
            resp = requests.get(url)
            res = resp.json()
            if res["errno"] == "0":
                for i in res["data"][0]:
                    dict = {}
                    dict["common_name"] = i["common_name"]
                    dict["result_score"] = i["result_score"]
                    score_list1.append(dict)
            else:
                print("接口错误")

        if i == 2:
            url = "http://outreach-partners-rating-api.turboradio.cn/export"
            resp = requests.get(url)
            res = resp.json()
            if res["errno"] == "0":
                for i in res["data"][0]:
                    dict = {}
                    dict["common_name"] = i["common_name"]
                    dict["result_score"] = i["result_score"]
                    score_list2.append(dict)
            else:
                print("接口错误")

    # print(score_list)
    # print(score_list1)

    error_list =[]
    for i in range(len(score_list)):
        if score_list[i]["result_score"] == score_list1[i]["result_score"] == score_list2[i]["result_score"]:
            pass
        else:
            error_list.append(score_list[i]["common_name"])
            # print(score_list[i], score_list1[i],score_list2[i])



    # print("连锁评分的连锁数量：", len(score_list))
    print("返回数据会变化的连锁：", error_list)
    print(len(error_list))
    #
    total = 0.00
    for i in range(0, len(score_list)):
        total = total + float(score_list[i]["result_score"])
    x = get_partner_common("4")
    print("返回的所有评分的和:", total, "连锁数:", x[0][0])
    print("数据质量总评分:", total / float(x[0][0]))



def test_itu_url():
    url = "http://outreach-partners-rating-api.turboradio.cn/export"
    resp = requests.get(url)
    res =resp.json()
    nub = len(res["data"][0])
    a = res["data"][0]
    print(nub)
    list_1 = []
    list_2 = []
    for i in range(len(a)):
        list_1.append(a[i]["target_item_list"]["1"][1]["result_score"])
        list_2.append(a[i]["target_item_list"]["2"][1]["result_score"])

    print(list_1)
    print(list_2)
    for i in range(len(list_1)):
        if (list_1[i] > 1) or (list_2[i] > 1):
            print(list_1[i])
            print(list_2[i])



def sum_goods():


    #获取所有连锁的cooperation
    cooperation_data = get_partner_common("2")
    cooperation_list = list(map(lambda x: x[0], cooperation_data))
    print(cooperation_list)
    goods_list = []
    stores_list = []
    for i in cooperation_list:
        goods = get_goods_partner(i)
        if goods:
            goods_list.append(goods[0][0])
    for i in cooperation_list:
        stores = get_store_partner(i)
        if stores:
            stores_list.append(stores[0][0])

    print(goods_list)
    print(stores_list)

    total = 0
    for i in range(len(goods_list)):
        total = total + goods_list[i]
    total_stores = 0
    for i in range(len(stores_list)):
        total_stores = total_stores + stores_list[i]

    return total, total_stores

if __name__ == '__main__':
    # a = count_partner()
    # b = count_goods_store()
    # c = total_quality_score()
    # d = test_itu_url()
    e,f = sum_goods()

    # print(a)
    # print(b)
    # print(d)
    print(e,f)
