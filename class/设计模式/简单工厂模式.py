class ShapeFactory(object):
    """工厂类"""

    def getShape(self):
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


class Shape(object):
    """
    接口类，负责决定创建哪个ShapeFactory的子类
    """

    def create(self, shape):
        if shape == 'Circle':
            return Circle()
        elif shape == 'Rectangle':
            return Rectangle()
        else:
            return None


if __name__ == "__main__":
    fac = Shape()
    obj = fac.create('Circle')
    obj.draw()
    obj.getShape()

# 简单工厂
# 工厂模式（Factory Pattern）是Java中最常用的设计模式之一。
# 这种类型的设计模式属于创建型模式，它提供了一种创建对象的最佳方式。
# 在工厂模式中，我们在创建对象时不会对客户端暴露创建逻辑，并且是通过使用一个共同的接口来指向新创建的对象。
#
# 意图：
# 定义一个用于创建对象的接口，让子类决定实例化哪一个类。Factory Method 使一个类的实例化延迟到其子类。
# 适用性：
# 当一个类不知道它所必须创建的对象的类的时候。
# 当一个类希望由它的子类来指定它所创建的对象的时候。
# 当类将创建对象的职责委托给多个子类中的某一个。


# 优点：客户端不需要修改代码。
# 缺点： 当需要增加新的运算类的时候，不仅需新加运算类，还要修改工厂类，违反了开闭原则。　　
