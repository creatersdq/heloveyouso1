from apps.core.test_date_base import session_maker
from apps.models.partners_table.partners_manage import PartnerConfig
from apps.models.partners_table.partners_common_cooperation import (Goods, StoreGoods)
import allure


@allure.step("修改config表配置")
def update_config(cooper: str, schemaName: str,value: str = None):
    """修改config表配置"""
    with session_maker() as db:
        find = db.query(PartnerConfig).filter(PartnerConfig.schemaName == schemaName,
                                              PartnerConfig.cooperation == cooper).first()

        if find:
            return db.query(PartnerConfig).filter(PartnerConfig.cooperation == cooper,
                                               PartnerConfig.schemaName == schemaName).update({"value": value})
        else:
            db.add(PartnerConfig(cooperation=cooper, schemaName=schemaName, value=value))


@allure.step("获取连锁对应的连锁库")
def get_goods_data(internal_id: str) -> str:
    """获取连锁对应的连锁库"""
    with session_maker() as db:
        goods_data = db.query(Goods).filter(Goods.internal_id == internal_id).all()
        return goods_data

@allure.step("修改门店下的商品上下架状态")
def updated_goods_data(goods_internal_id: str,group_id: str, value: int):
    """修改门店下的商品上下架状态"""
    with session_maker() as db:
        db.query(StoreGoods).filter(StoreGoods.goods_internal_id == goods_internal_id,
                                    StoreGoods.group_id == group_id).update({"status": value})
