# PO分层文件
from selenium.webdriver.common.by import By
from apps.ui_auto.core.base_page import BasePage, BaseHandler


# 登录页面对象库层
class LoginPage(BasePage):

    # 1.定义初始化方法，初始化方法需要先定义好界面需要操作的元素对象
    # 2.实现获取这些定义好的元素的方法
    def __init__(self):
        # 重写父类的初始化方法，其实就是获取浏览器驱动对象
        super().__init__()
        # 登录按钮
        self.submit_btn = (By.XPATH, "//span[text()='登录']")
        # 用户名输入框
        self.username = (By.XPATH, "//input[@placeholder='请输入用户名或邮箱']")
        # 密码输入框
        self.password = (By.XPATH, "//input[@placeholder='请输入密码']")
        # 立即登录按钮
        self.login_btn = (By.XPATH, "//span[text()='立即登录']")

    # 获取登录按钮的元素对象
    def find_submit_btn(self):
        return self.find_element(self.submit_btn)

    # 获取用户名输入框的元素对象
    def find_username(self):
        return self.find_element(self.username)

    # 获取密码输入框的元素对象
    def find_password(self):
        return self.find_element(self.password)

    # 获取立即登录的元素对象
    def find_login_btn(self):
        return self.find_element(self.login_btn)


# 操作层
# 操作层需要对页面的元素进行操作，就需要获取的元素对象，直接调用对象库层的查找元素对象的方法
class LoginHandler(BaseHandler):

    # 定义初始化方法，用来实例化对象库层类
    def __init__(self):
        self.login_page = LoginPage()

    # 点击登录
    def click_submit_btn(self):
        self.login_page.find_submit_btn().click()

    # 输入用户名
    def input_username(self, username):
        # 清空默认用户名输入框的信息
        self.input_text(self.login_page.find_username(), username)

    # 输入密码
    def input_password(self, pwd):
        # 清空默认密码输入框的信息
        self.input_text(self.login_page.find_password(), pwd)

    # 点击立即登录按钮
    def click_login_btn(self):
        self.login_page.find_login_btn().click()


# 业务层
# 目的是用来组装业务流程
class LoginProxy:

    def __init__(self):
        self.login_handler = LoginHandler()

    # 登录业务完整操作
    def login(self, username, pwd):
        # 点击登录
        self.login_handler.click_submit_btn()
        # 输入用户名
        self.login_handler.input_username(username)
        # 输入密码
        self.login_handler.input_password(pwd)
        # 点击立即登录
        self.login_handler.click_login_btn()
