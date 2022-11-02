from apps.cases.common.partners_common.normal_partners_push.produc_chain import ProChainConn
from apps.extensions.read_yml import file_yml
import datetime,random

partners_push = file_yml("partners_common/datas/partners_data_push.yml")
pro_chain = ProChainConn()

'''获取数据来源组装列表'''
class GetDatas:

    def __init__(self):
        self.drugs = partners_push["drugs"]
        self.stock = partners_push["stock"]
        self.categorys = partners_push["categorys"]
        self.members = partners_push["members"]
        self.dantidianstores = partners_push["dantidianstores"]
        self.orders = partners_push["orders"]
        self.store = partners_push["stores"]

    def goods_datas(self,start,end,groupid,num,tags):
        sql = "select * from partner_common_143.standard_goods order by id asc  limit %d" %num
        dates = pro_chain.exec_sql(sql)
        druglist = []
        for i in range(len(dates)):
            a = start
            i = i + a
            if i < end and start <= i:
                self.drugs["id"] = dates[i][1]
                self.drugs["goods_no"] = dates[i][1]
                self.drugs["memory_code"] = "haha@comzhujima"
                self.drugs["name"] = dates[i][2]
                self.drugs["code"] = dates[i][3]
                self.drugs["number"] = dates[i][4]
                price = round(random.uniform(1, 10), 2)
                self.drugs["price"] = str(price)
                self.drugs["member_price"] = random.choice([str(round(random.uniform(1, price), 2)),'0','0.0','0.00',''])
                self.drugs["yellow_flag"] = random.choice(['0','1',''])
                self.drugs["pack"] = dates[i][6]
                self.drugs["manufacturer"] = dates[i][8]+random.choice('helloPythonsuying')
                self.drugs["form"] = dates[i][5]
                self.drugs["status"] = str(random.randint(0, 1))
                self.drugs["group_id"] = groupid
                self.drugs["category_id"] = ["sy123456"]
                self.drugs["tags"] = tags
                druglist.append(self.drugs.copy())
            else:
                break
        return druglist

    def stock_datas(self,start, end, storeid,num):
        sql = "select * from partner_common_143.standard_goods limit %d" %num
        dates = pro_chain.exec_sql(sql)
        stock_list = []
        for y in range(len(dates)):
            a = start
            y = y + a
            if start <= y and y < end:
                self.stock["drug_id"] = dates[y][1]
                self.stock["quantity"] = str(random.randint(0, 999))
                self.stock["status"] = str(random.randint(0, 1))
                self.stock["store_id"] = storeid
                stock_list.append(self.stock.copy())
            else:
                break
        return stock_list

    def categorys_datas(self,num):
        categorys_list = []
        for i in range(num):
            category_id = str(datetime.datetime.now().strftime('%Y%m%d'))
            for a in range(5):
                category_id = category_id + str(random.choice([random.randint(0, 9),chr(random.randint(97, 122)),random.randint(65, 90)]))
            self.categorys["category_id"] = category_id
            self.categorys["levels"] = str(random.randint(0, 1234))
            self.categorys["status"] = str(random.randint(0, 1))
            self.categorys["sort"] = str(random.randint(0, 9999))
            categorys_list.append(self.categorys.copy())
        return categorys_list

    def members_datas(self,num):
        members_list = []
        for i in range(num):
            code = "820201"
            for a in range(10):
                code = code + str(random.randint(0, 9))
            self.members["card_number"] = code
            members_list.append(self.members.copy())
        return members_list

    def dantidian_stores_datas(self,cooper,start,end,num):
        sql = "select * from partner_common_151.stores ORDER BY RAND() limit  %d" %num
        dates = pro_chain.exec_sql(sql)
        dantidian_stores_list = []
        for x in range(len(dates)):
            a = start
            x = x + a
            if start <= x and x < end:
                self.dantidianstores["id"] = dates[x][1]
                self.dantidianstores["name"] = dates[x][3]
                self.dantidianstores["number"] = dates[x][4]
                self.dantidianstores["status"] = str(random.randint(0, 1))
                self.dantidianstores["address"] = dates[x][5]+random.choice('helloPythonsuying')
                self.dantidianstores["group_id"] = dates[x][1]
                self.dantidianstores["roomId"] = cooper
                self.dantidianstores["full_name"] = dates[x][3]
                dantidian_stores_list.append(self.dantidianstores.copy())
            else:
                break
        return dantidian_stores_list

    def normal_stores_datas(self, start, end,num):
        sql = "select * from partner_common_10.stores where number != \'\' order by id desc  limit  %d" %num
        dates = pro_chain.exec_sql(sql)
        normal_stores_list = []
        for x in range(len(dates)):
            a = start
            x = x + a
            if start <= x and x < end:
                self.store["group_id"] = dates[x][2]
                self.store["id"] = dates[x][1]
                self.store["name"] = dates[x][3]
                self.store["number"] = dates[x][4]
                self.store["status"] = str(random.randint(0, 1))
                self.store["address"] = dates[x][5]+ random.choice('helloPythonsuying')
                normal_stores_list.append(self.store.copy())
            else:
                break
        return normal_stores_list


    def normal_orders_datas(self,storeid,num):
        normal_orders_list = []
        for i in range(num):
            day = datetime.datetime.now().strftime('%Y%m%d')
            orderId = str(day)
            for x in range(10):
                orderId = orderId + str(random.randint(0, 9))
            self.orders["id"] = orderId
            self.orders["order_no"] = orderId[4:15]
            self.orders["store_id"] = storeid
            normal_orders_list.append(self.orders.copy())
        return normal_orders_list

# num = 2
# a = GetDatas().normal_stores_datas(2,4,4)
# print(a)

# a = {'requestHead': {'cooperation': '2020102600000092901019', 'nonce': '87DF487E42ADDC3AF42B3FF5F3B2105F', 'sign': 'e633733b253f526945eb26e46325c59ce9e87253', 'timestamp': '1607309630'}, 'channel': '1', 'stores': [{'id': '0420114847h', 'number': '7494', 'full_name': '乌兰浩特翘楚店0420114847', 'address': '内蒙古省乌兰浩特市和平街锦绣家园小区5号楼商住楼17号商业门市号e', 'phone': '37483274110119', 'group_id': '0420114847h', 'status': '0', 'create_time': '2021-04-12 13:51:47', 'update_time': '2021-04-12 13:53:56', 'province': '湖南省17', 'city': '怀化市17', 'area': '芷江侗族自治县17', 'business_time': '00:00-23:59', 'name': '乌兰浩特翘楚店0420114847', 'firstPinyin': 'ygsh', 'pinyin': 'ceshishanghumendian', 'areaCode': '431200', 'dutyMan': '19903262122', 'dutyIphone': '19903262122', 'roomId': '2020112500000038507328', 'uniondrug_store_id': '', 'RoomID': '2020102600000092901019'}]}
# import json
# print(json.dumps(a))