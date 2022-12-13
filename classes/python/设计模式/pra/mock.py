# _*_coding:utf-8_*_

class MockFactory(object):
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

    def api_insure(self):
        print("保司投保接口标准返回")

    def api_claim(self):
        print("保司理赔接口标准返回")


class Ypb(MockFactory):
    # 继承父类__init__并重写
    def __init__(self, dev):
        super(Ypb, self).__init__(dev)
        self.product = "YPB"

    def order(self):
        print("药品保-订单数据mock")

    def claim(self):
        print("药品保-理赔数据mock")

    def invoice(self):
        print("药品保-理赔发票数据mock")

    def order_attachments(self):
        print("药品保-订单影像件数据mock")

    def pay_info(self):
        print("药品保-理赔反洗钱数据mock")


class Guarantee(MockFactory):
    # 继承父类__init__并重写
    def __init__(self, dev):
        super(Guarantee, self).__init__(dev)
        self.product = "Guarantee"

    def order(self):
        print("保障-订单数据mock")

    def claim(self):
        print("保障-理赔数据mock")


class MockInterfaceFactory(object):
    """
    接口基类
    """

    def create(self, dev):
        """
        把要创建的工厂对象装配进来
        """
        raise NotImplementedError


class MockYpb(MockInterfaceFactory):
    def create(self, dev):
        return Ypb(dev)


class MockGuarantee(MockInterfaceFactory):
    def create(self, dev):
        return Guarantee(dev)


if __name__ == "__main__":
    mock_ypb_interface = MockYpb()
    obj = mock_ypb_interface.create(dev="name")
    print(obj.product)
    # obj.get_product_type()
    # obj.api_insure()
    # obj.order()

    mock_guarantee_interface = MockGuarantee()
    obj2 = mock_guarantee_interface.create(dev="fee")
    obj2.product = "YPB"
    print(obj2.product)
    # obj2.get_product_type()
    # obj2.api_insure()
    # obj2.order()
