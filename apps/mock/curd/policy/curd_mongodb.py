import pymongo

from apps.core.mongo_client import MongoDBClient
from apps.extensions.logger import log


def get_mongodb_log(
        collections: str,
        key: str,
        value: str,
        dev: str
) -> dict:
    """
    根据关键字查询mongodb
    :param collections:查询集合
    :param key:匹配字段
    :param value:匹配内容
    :param dev:环境
    :return:
    """
    try:
        # 获取mongodb连接
        mongodb_connect = MongoDBClient().get_mongo_conn(dev)
        # 连接mongodb数据库
        policy_data = mongodb_connect['module_equity_claim'][collections]
        # 正则
        t = "." + value + ".*"
        # 查询-正则匹配/关键字匹配
        data = policy_data.find_one({key: {'$regex': t}}, sort=[('_id', pymongo.DESCENDING)])
        res = {}
        for i in data:
            if i == "originRequest":
                res["originRequest"] = data[i]
            elif i == "originResponse":
                res["originResponse"] = data[i]
        return res
    except Exception as e:
        log.get_log(
            "policy_db_action",
            "ERROR",
            "mongodb查询失败:{}".format(e)
        )


if __name__ == '__main__':
    c = get_mongodb_log(
        collections='UniondrugSynGroupV3_0_policyDownload',
        key='originRequest',
        value="PN165104111912177720939351862031",
        dev='test'
    )
    print(c)
    # print(type(c))
