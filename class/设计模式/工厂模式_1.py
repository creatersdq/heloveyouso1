# _*_coding:utf-8_*_

# 工厂模式
class ShapeFactory(object):
    """工厂类"""

    def get_shape(self):
        return self.shape_name


class Circle(ShapeFactory):

    def __init__(self):
        self.shape_name = "Circle"

    def draw(self):
        print('draw circle')


class Rectangle(ShapeFactory):
    def __init__(self):
        self.shape_name = "Retangle"

    def draw(self):
        print('draw Rectangle')


class ShapeInterfaceFactory(object):
    """接口基类"""

    def create(self):
        """把要创建的工厂对象装配进来"""
        raise NotImplementedError


class ShapeCircle(ShapeInterfaceFactory):
    def create(self):
        return Circle()


class ShapeRectangle(ShapeInterfaceFactory):
    def create(self):
        return Rectangle()


if __name__ == "__main__":
    shape_interface = ShapeCircle()
    obj = shape_interface.create()
    obj.get_shape()
    obj.draw()

    shape_interface2 = ShapeRectangle()
    obj2 = shape_interface2.create()
    obj2.draw()


# 这个和简单工厂有区别，简单工厂模式只有一个工厂，工厂方法模式对每一个产品都有相应的工厂
# 　　好处：增加一个运算类（例如N次方类），只需要增加运算类和相对应的工厂，两个类，不需要修改工厂类。
# 　　缺点：增加运算类，会修改客户端代码，工厂方法只是把简单工厂的内部逻辑判断移到了客户端进行。



