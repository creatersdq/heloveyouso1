# coding=utf-8

from selenium import webdriver

driver = webdriver.Chrome()

driver.get("http://www.baidu.com")

driver.maximize_window()  # 将浏览器最大化显示

driver.set_window_size(480, 800)  # 设置浏览器宽480、高800显示"

driver.back()  # 后退

driver.forward()  # 前进

driver.close()  # 关闭chrome

driver.quit()  # 退出chrome
