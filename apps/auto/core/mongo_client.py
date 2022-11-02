import pymongo

class MongoDBClient:

    def __init__(self):
        self.mgdb_conn = pymongo.MongoClient('mongodb://adminUser:juyin#2020@192.168.3.26:27017/admin', connect=False, maxPoolSize=2000)

    def get_mongo_conn(self):
        return self.mgdb_conn

MongoConnect = MongoDBClient().get_mongo_conn()