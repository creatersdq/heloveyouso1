from apps.db_actions.partners_stock_actions import update_config


'''修改config表的配置信息'''
class ModifyConfig:

    def __init__(self):
        pass

    def creat_config_scene(self,cooper,case_type):
        if case_type == 2: # 只配置了stockShelve = 1
            update_config(cooper=cooper, schemaName='stockShelve', value='1')
            update_config(cooper=cooper, schemaName='yellowFlag', value='0')
            update_config(cooper=cooper, schemaName='oneShopOnePrice', value='0')
            update_config(cooper=cooper, schemaName='pushStockToMongo', value='0')
        elif case_type == 3: # 只配置了oneShopOnePrice = 1
            update_config(cooper=cooper, schemaName='stockShelve', value='0')
            update_config(cooper=cooper, schemaName='yellowFlag', value='0')
            update_config(cooper=cooper, schemaName='oneShopOnePrice', value='1')
            update_config(cooper=cooper, schemaName='pushStockToMongo', value='0')
        elif case_type == 4: # 只配置了oneShopOnePrice = 1和 stockShelve = 1
            update_config(cooper=cooper, schemaName='stockShelve', value='1')
            update_config(cooper=cooper, schemaName='yellowFlag', value='0')
            update_config(cooper=cooper, schemaName='oneShopOnePrice', value='1')
            update_config(cooper=cooper, schemaName='pushStockToMongo', value='0')
        elif case_type == 5: # 只配置了pushStockToMongo = 1
            update_config(cooper=cooper, schemaName='stockShelve', value='0')
            update_config(cooper=cooper, schemaName='yellowFlag', value='0')
            update_config(cooper=cooper, schemaName='oneShopOnePrice', value='0')
            update_config(cooper=cooper, schemaName='pushStockToMongo', value='1')
        elif case_type == 6: # 只配置了oneShopOnePrice = 1和 pushStockToMongo = 1
            update_config(cooper=cooper, schemaName='stockShelve', value='0')
            update_config(cooper=cooper, schemaName='yellowFlag', value='0')
            update_config(cooper=cooper, schemaName='oneShopOnePrice', value='1')
            update_config(cooper=cooper, schemaName='pushStockToMongo', value='1')
        elif case_type == 7:# 只配置了stockShelve = 1和 pushStockToMongo = 1
            update_config(cooper=cooper, schemaName='stockShelve', value='1')
            update_config(cooper=cooper, schemaName='yellowFlag', value='0')
            update_config(cooper=cooper, schemaName='oneShopOnePrice', value='0')
            update_config(cooper=cooper, schemaName='pushStockToMongo', value='1')
        elif case_type == 8: # 全都配置了，yellowFlag = 1
            update_config(cooper=cooper, schemaName='stockShelve', value='1')
            update_config(cooper=cooper, schemaName='yellowFlag', value='1')
            update_config(cooper=cooper, schemaName='oneShopOnePrice', value='1')
            update_config(cooper=cooper, schemaName='pushStockToMongo', value='1')
        elif case_type == 9: # 只配置了yellowFlag = 0.88
            update_config(cooper=cooper, schemaName='stockShelve', value='0')
            update_config(cooper=cooper, schemaName='yellowFlag', value='0.88')
            update_config(cooper=cooper, schemaName='oneShopOnePrice', value='0')
            update_config(cooper=cooper, schemaName='pushStockToMongo', value='0')
        elif case_type == 10: # 只配置了yellowFlag = 0.88 和 oneShopOnePrice = 1
            update_config(cooper=cooper, schemaName='stockShelve', value='0')
            update_config(cooper=cooper, schemaName='yellowFlag', value='0.88')
            update_config(cooper=cooper, schemaName='oneShopOnePrice', value='1')
            update_config(cooper=cooper, schemaName='pushStockToMongo', value='0')
        else: # 什么配置都没有
            update_config(cooper=cooper, schemaName='stockShelve', value='0')
            update_config(cooper=cooper, schemaName='yellowFlag', value='0')
            update_config(cooper=cooper, schemaName='oneShopOnePrice', value='0')
            update_config(cooper=cooper, schemaName='pushStockToMongo', value='0')

# ModifyConfig().creat_config_scene('2020102600000092901019','1')