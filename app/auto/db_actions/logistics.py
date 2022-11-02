from apps.core.test_date_base import session_maker
from apps.models.logistics_table.database_module_outreach_express import StoresTable, StoreRecordsTable, OrdersTable, \
    OrderSendsTable, OrderRiderTable, OrderCancel


# 查询orders表的status
def get_orders_status(order_no):
    with session_maker() as db:
        result = db.query(OrdersTable).filter(OrdersTable.orderNo == order_no).first()
        if result:
            return result.status
        else:
            return None


# 查询order_sends表的status
def get_order_sends_status(order_no, mark):
    with session_maker() as db:
        result = db.query(OrderSendsTable).filter(OrderSendsTable.orderNo == order_no,
                                                  OrderSendsTable.cooperate == mark).first()
        if result:
            return result.status
        else:
            return None


# 查询order_rider表的riderId
def get_order_rider_rider_id(order_no):
    with session_maker() as db:
        result = db.query(OrderRiderTable).filter(OrderRiderTable.orderNo == order_no).first()
        if result:
            return result.riderId
        else:
            return None


# 查询order_rider表的status
def get_order_rider_status(order_no):
    with session_maker() as db:
        result = db.query(OrderRiderTable).filter(OrderRiderTable.orderNo == order_no).first()
        if result:
            return result.status
        else:
            return None


# 查询order_cancel表是否新增了两条数据(达达，美团，顺丰，三个物流有一个接单，其余两个会在order_cancel表中插入记录)
def get_order_cancel_code(order_no):
    with session_maker() as db:
        result = db.query(OrderCancel).filter(OrderCancel.orderNo == order_no).all()
        return len(result)


# 查询orders表的retryTimes字段是否为1(重发次数为1)
def get_orders_retry_times(order_no):
    with session_maker() as db:
        result = db.query(OrdersTable).filter(OrdersTable.orderNo == order_no).first()
        if result:
            return result.retryTimes
        else:
            return None


# 查询orders_rider的outNo
def get_order_rider_out_code(order_no):
    with session_maker() as db_01:
        result_out_no = db_01.query(OrderRiderTable).filter(OrderRiderTable.orderNo == order_no).first()
        if result_out_no:
            return result_out_no.outNo
        else:
            return None


# 查询order_cancel 的outCode
def get_order_cancel_out_code(order_no):
    # 获取order_rider表中的三方订单号作为order_cancel表的查询条件
    order_out_no = get_order_rider_out_code(order_no)
    with session_maker() as db:
        result = db.query(OrderCancel).filter(OrderCancel.outNo == order_out_no).first()
        if result:
            return result.outCode
        else:
            return None


# 查询store_records表中是否有新增门店的记录
def get_store_records_is_have(store_id):
    with session_maker() as db:
        result = db.query(StoreRecordsTable).filter(StoreRecordsTable.storeId == store_id).all()
        return result


# 查询order_sends表中的outNo字段
def get_order_sends_out_no(order_no):
    with session_maker() as db:
        result = db.query(OrderSendsTable).filter(OrderSendsTable.orderNo == order_no,
                                                  OrderSendsTable.cooperate == 'meituan').first()
        if result:
            return result.outNo
        else:
            return None


# 查询orders表中的cooperate字段是否为meituan
def get_orders_cooperate(order_no):
    with session_maker() as db:
        result = db.query(OrdersTable).filter(OrdersTable.orderNo == order_no).first()
        if result:
            return result.cooperate
        else:
            return None


if __name__ == '__main__':
    # res = get_order_sends_status('20201230095737669279','meituan')
    res = get_orders_status('2020121718073031580')
    # res = get_store_records("12344321")
    # res = get_order_rider_status('20201217180730391580')
    # res = get_order_cancel_code('20201230101802673596')
    # res = get_order_sends_out_no('202012041502345237081')
    # res = get_store_records_is_have('7590')
    # res = get_orders_retry_times('20201222095800122257')
    # res = get_order_rider_rider_id('20201222095512715551')
    # res = get_orders_cooperate('202012041502345237011')
    # res=get_orders_status('20210113135405824513')
    # res = get_order_sends_status('20210113154341298587', 'dada')
    print(res, type(res))
    if res == 0:
        print("等于0")
    else:
        print("为None")

    # create_case("www.baidu.com", 'application/json', 'testcase/data', 'POST', 12, 'logistics_common', '物流', '通过')
