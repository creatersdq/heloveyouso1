# 工具类
import time
from selenium import webdriver


# 定义浏览器驱动获取和关闭的类
# 减少多个用例都调用的实例化浏览器驱动以及最大化和隐式等待的方法，减少部分代码冗余
class DriverUtil:
    # 私有变量，用来存储浏览器驱动对象
    __driver = None

    is_open = True

    # 获取浏览器驱动
    # 1.用类级别定义方法的目的是为了方便测试用例的代码的调用
    # 2.为了防止测试用例里面多次调用获取浏览器驱动的方法，导致多个浏览器驱动，加上判断浏览器是否为空的判断
    @classmethod
    def get_driver(cls):
        if cls.__driver is None:
            cls.__driver = webdriver.Chrome()
            cls.__driver.maximize_window()
            cls.__driver.implicitly_wait(10)
        return cls.__driver

    # 关闭浏览器驱动
    # 1.增加判断浏览器驱动是否为空的判断，如果为空，则不执行关闭
    @classmethod
    def quit_dirver(cls):
        if cls.is_open and cls.__driver is not None:
            time.sleep(2)
            cls.get_driver().quit()
            cls.__driver = None


# 窗口切换的方法
def switch_window():
    driver = DriverUtil.get_driver()
    handlers = driver.window_handles
    driver.switch_to.window(handlers[-1])
