# _*_coding:utf-8_*_

class ActionFactory(object):
    """
    工厂类
    """

    def __init__(self, dev):
        self._dev = dev
        self._product_type: str = ""

    @property
    def product(self):
        return self._product_type

    @product.setter
    def product(self, product_type):
        if not isinstance(product_type, str):
            raise ValueError('dev must be an string!')
        if product_type not in ("YPB", "Guarantee"):
            raise ValueError('dev must in  (YPB,Guarantee)!')
        self._product_type = product_type

    def server_conn(self):
        print("连接服务器")


class Ypb(ActionFactory):
    # 继承父类__init__并重写
    def __init__(self, dev):
        super(Ypb, self).__init__(dev)
        self.product = "YPB"

    def push_claim_invoice(self):
        print("push_claim_invoice")

    def push_claim_image(self):
        print("push_claim_image")

    def query_finance_pool(self):
        print("query_finance_pool")

    def query_insure_task(self):
        print("query_insure_task")

    def query_insure_result(self):
        print("query_insure_result")

    def reset_lock_plan_log(self):
        print("reset_lock_plan_log")


class Guarantee(ActionFactory):
    # 继承父类__init__并重写
    def __init__(self, dev):
        super(Guarantee, self).__init__(dev)
        self.product = "Guarantee"


class ActionsInterfaceFactory(object):
    """
    接口基类
    """

    def create(self, dev):
        """
        把要创建的工厂对象装配进来
        """
        raise NotImplementedError


class ActionsYpb(ActionsInterfaceFactory):
    def create(self, dev):
        return Ypb(dev)


class ActionsGuarantee(ActionsInterfaceFactory):
    def create(self, dev):
        return Guarantee(dev)


if __name__ == "__main__":
    a = ActionsYpb()
    obj = a.create(dev="test")
    print(obj.product)
    # obj.get_product_type()
    # obj.api_insure()
    # obj.order()

    b = ActionsGuarantee()
    obj2 = b.create(dev="test")
    obj2.product = "YPB"
    print(obj2.product)
    # obj2.get_product_type()
    # obj2.api_insure()
    # obj2.order()
