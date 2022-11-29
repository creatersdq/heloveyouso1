import os
import logging.handlers

# os.path.abspath(__file__) 获取当前文件完整路径的方法
# os.path.dirname(os.path.abspath(__file__))获取当前文件完整路径的目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# 日志配置方法
def log_basic():
    # 1.创建日志器,项目中创建日志器不要定义名称，默认为root
    logger = logging.getLogger()
    # 2.设置日志级别
    logger.setLevel(level=logging.INFO)
    # 3.创建处理器
    ls = logging.StreamHandler()  # 打印到控制台的处理器
    file_name = BASE_DIR + '/log/test.log'
    lht = logging.handlers.TimedRotatingFileHandler(filename=file_name, when='midnight', interval=1,backupCount=2)  # 按时间分隔日志文件的处理器
    # 4.创建格式化器
    fmt_str = "%(asctime)s %(levelname)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
    fomatter = logging.Formatter(fmt=fmt_str)
    # 5.将格式化器添加到处理器
    ls.setFormatter(fomatter)
    lht.setFormatter(fomatter)
    # 6.将处理器添加到日志器
    logger.addHandler(ls)
    logger.addHandler(lht)
