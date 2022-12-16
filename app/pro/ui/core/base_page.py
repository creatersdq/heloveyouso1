# 基类文件
from app.pro.ui.core.utils import DriverUtil


# 创建对象库层的基类
class BasePage:

    def __init__(self):
        self.driver = DriverUtil.get_driver()

    # 定位元素
    # 抽取共性的代码
    # 基类的方法最终还是提供给这些共性的代码来使用
    def find_element(self, location):
        return self.driver.find_element(*location)

    def open_url(self, url):
        return self.driver.get(url)

    # 创建操作层的基类


class BaseHandler:
    # 输入文本
    def input_text(self, element, text):
        # 清空默认用户名输入框的信息
        # 1.元素对象在po的对象库层可以获取到
        # 2.共性的方法是供子类调用
        element.clear()
        element.send_keys(text)
