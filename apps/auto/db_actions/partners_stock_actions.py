from apps.core.test_date_base import session_maker
from sqlalchemy.sql.expression import func
from apps.models.partners_table.partners_common_cooperation import GoodsStock, Stores, Goods, StoreGoods, EshopGoods, EshopGoodsStock
from apps.models.partners_table.partners_manage import PartnerConfig, Partners, PartnersPoint
from apps.extensions.logger import log
import allure



@allure.step("查询连锁指向关系")
def get_point(cooper: str) -> str:
    '''获取point表'''
    with session_maker() as db:
        point = db.query(PartnersPoint).filter(PartnersPoint.cooperation == cooper).first()
        if point is None:
            return cooper
        elif point.configType == 2:
            return point.nickCooperation
        else:
            return cooper

@allure.step("获取数据库中连锁的config信息，把内容返回成字典类型")
def get_config(cooper: str) -> dict:
    '''获取数据库中连锁的config信息，把内容返回成字典类型'''
    with session_maker() as db:
        config = db.query(PartnerConfig).filter(PartnerConfig.cooperation == cooper).all()
        config_dict = {}
        for i in range(len(config)):
            config_dict[config[i].schemaName] = str(config[i].value)
        return config_dict


def update_config(cooper:str,schemaName:str,value:str):
    '''更新config表中的数据'''
    with session_maker() as db:
        find = db.query(PartnerConfig).filter(PartnerConfig.schemaName == schemaName,PartnerConfig.cooperation == cooper).first()
        if find == None:
            db.add(PartnerConfig(cooperation = cooper,
                                 schemaName = schemaName,
                                 value = value))
        else:
            db.query(PartnerConfig).filter(PartnerConfig.schemaName == schemaName,
                                                    PartnerConfig.cooperation == cooper).update({"value":value})


def get_dbname(cooper: str) -> str:
    '''获取连锁对应的连锁库'''
    with session_maker() as db:
        dbname = db.query(Partners).filter(Partners.cooperation == cooper).first().dbname
        return dbname


def get_stores() -> list:
    '''获取门店内码和价格组'''
    with session_maker() as db:
        stores = db.query(Stores.internal_id,Stores.group_id).order_by(func.rand()).limit(3).all()
        stores_list = list(map(lambda x:{"internal_id":x[0],"group_id":x[1]},stores))
        return stores_list


def get_goods(cooper:str, groupid: str) ->list:
    '''根据门店的价格组获取相应的商品信息'''
    dbname = get_dbname(cooper)
    with session_maker() as db:
        goods = db.execute('''
SELECT
	a.*,
	b.group_id,
	b.price,
	b.status,
	b.member_price
FROM
	{0}.goods a,
	{0}.store_goods b 
WHERE
	a.internal_id = b.goods_internal_id
	AND trade_code != 'NULL'
	AND trade_code != ''
	AND b.group_id = {1} ORDER BY RAND() limit 1
        '''.format(dbname,groupid))
        return list(goods)

@allure.step("从数据库中获取库存数据")
def get_stock(storeid:str,goodsid:list) -> list:
    '''获取数据库中的库存'''
    with session_maker() as db:
        stocks = db.query(GoodsStock.store_internal_id,
                          GoodsStock.goods_internal_id,
                          GoodsStock.stock_quantity).filter(GoodsStock.store_internal_id==storeid,GoodsStock.goods_internal_id.in_(goodsid)).all()
        res = list(map(lambda x: {"store_internal_id": x[0], "goods_internal_id": x[1], "stock_quantity": x[2]}, stocks))
    log.get_log("partners_stocks/stock_data", "INFO", "从数据库中获取的库存：{}".format(res))
    return res


def from_store_goods_status(storeid:str,goodsid:str):
    '''获取store_goods表的商品状态'''
    with session_maker() as db:
        status_data = db.query(StoreGoods).filter(StoreGoods.group_id == storeid,StoreGoods.goods_internal_id== goodsid).first()
        if status_data != None:
            return status_data.status
        else:
            return None

def from_goods_status(goodsid:str):
    '''获取电商goods表中的商品状态'''
    with session_maker() as db:
        status_data = db.query(EshopGoods).filter(EshopGoods.internal_id == goodsid).first()
        if status_data != None:
            return status_data.status
        else:
            return None

@allure.step("获取电商goods表的商品id")
def get_eshop_goods() -> list:
    '''获取电商goods表的商品数据'''
    with session_maker() as db:
        goods = db.query(EshopGoods.internal_id).order_by(func.rand()).limit(3).all()
        goods_list = [i[0] for i in goods]
        return goods_list

def get_eshop_stock(storeid:str,goodsid:str):
    '''获取电商的库存数据'''
    with session_maker() as db:
        quantity = db.query(EshopGoodsStock).filter(EshopGoodsStock.store_internal_id == storeid,
                                                     EshopGoodsStock.goods_internal_id == goodsid).first()
        if quantity != None:
            return quantity.stock_quantity
        else:
            return None


# stockSearch_path = 'https://ebusiness.guodadrugstores.com/npserver/InterfaceServlet.do'
# update_config(cooper='shanghaiguoda', schemaName='stockSearch', value=stockSearch_path)

# print(from_goods_status("2139310"))
# print(get_eshop_stock('',"440013"))

