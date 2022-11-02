from apps.cases.common.partners_common.normal_partners_push.create_data_push import GetDatas
from apps.extensions.read_yml import file_yml

partners_push = file_yml("partners_common/datas/partners_data_push.yml")
get_datas = GetDatas()

'''造入参的数据，不包含村医和益丰等连锁'''
class PushCreate:

    def __init__(self):
        pass

    def goods_push(self,cooper,start, end, groupid,key,tags,num,channel='1'):
        '''推送商品'''
        common_body = partners_push["push_common"].copy()
        common_body["requestHead"]["cooperation"] = cooper
        goods_list = get_datas.goods_datas(start,end,groupid,num,tags)
        common_body["channel"] = channel
        common_body[key] = goods_list
        return common_body

    def stock_push(self, cooper, start, end, storeid,key,num, channel='1'):
        '''推送库存'''
        common_body = partners_push["push_common"].copy()
        common_body["requestHead"]["cooperation"] = cooper
        stock_list = get_datas.stock_datas(start,end,storeid,num)
        common_body["channel"] = channel
        common_body[key] = stock_list
        return common_body

    def categorys_push(self,cooper,num,key,channel='1'):
        '''推送类目'''
        common_body = partners_push["push_common"].copy()
        common_body["requestHead"]["cooperation"] = cooper
        categorys_list = get_datas.categorys_datas(num)
        common_body["channel"] = channel
        common_body[key] = categorys_list
        return common_body

    def members_push(self,cooper,num,key,channel='1'):
        '''推送会员，目前村医没有推送会员'''
        common_body = partners_push["push_common"].copy()
        common_body["requestHead"]["cooperation"] = cooper
        members_list = get_datas.members_datas(num)
        common_body["channel"] = channel
        common_body[key] = members_list
        return common_body

    def dantidian_stores_push(self, cooper, start, end,key,num,channel= '1'):
        '''单体店的门店推送'''
        common_body = partners_push["push_common"].copy()
        common_body["requestHead"]["cooperation"] = cooper
        common_body["channel"] = channel
        dantidian_stores_list = get_datas.dantidian_stores_datas(cooper,start,end,num)
        common_body[key] = dantidian_stores_list
        return common_body

    def normal_stores_push(self, cooper, start, end,num,key,channel='1'):
        '''普通连锁的门店推送'''
        common_body = partners_push["push_common"].copy()
        common_body["requestHead"]["cooperation"] = cooper
        common_body["channel"] = channel
        normal_stores_list = get_datas.normal_stores_datas(start, end,num)
        common_body[key] = normal_stores_list
        return common_body

    def orders_push(self, cooper, num, storeid,key, channel='1'):
        common_body = partners_push["push_common"].copy()
        common_body["requestHead"]["cooperation"] = cooper
        common_body["channel"] = channel
        normal_orders_list = get_datas.normal_orders_datas(storeid, num)
        common_body[key] = normal_orders_list
        return common_body

