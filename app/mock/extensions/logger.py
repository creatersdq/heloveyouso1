import json
import time
from loguru import logger
import os
from pathlib import Path
import logging


class Logger:
    #   rotation 日志创建时机，500mb 代表 当日志文件超过500mb时 将会自动创建新的
    # enqueue 是否异步生成
    # retention 日志最长保留时间 "1 week, 3 days"、"2 months"
    # __handler_id 默认日志不显示终端

    #     def __init__(self):
    #         self.rotation = "500MB"
    #         self.enqueue = False
    #         self.retention = "10 days"
    #         self.project_path = os.path.dirname(os.path.dirname(__file__))
    #         self.log_path = Path(self.project_path, "log")
    #         self.t = time.strftime("%Y_%m_%d")
    #         # self.format = "{time} {level} {module} {message}" 自定义日志格式,此处使用默认
    #         # print(self.project_path)
    #
    #     def get_log(self, parent, level, msg):
    #         logger.remove()
    #         try:
    #             os.makedirs(self.log_path / parent, 0o777)
    #         except FileExistsError:
    #             pass
    #         logger.add(f"{self.log_path}/{parent}/{self.t}.log", rotation=self.rotation,
    #                    encoding="utf-8", enqueue=self.enqueue,
    #                    retention=self.retention)
    #
    #         if level == "INFO":
    #             logger.info(msg)
    #         elif level == "WARNING":
    #             return logger.warning(msg)
    #         elif level == "DEBUG":
    #             return logger.debug(msg)
    #         elif level == "ERROR":
    #             return logger.error(msg)
    #         else:
    #             return logger.info(msg)
    #
    #
    # log = Logger()
    def __init__(self):
        self.rotation = "500MB"
        self.enqueue = False
        self.retention = "10 days"
        self.project_path = os.path.dirname(os.path.dirname(__file__))
        self.log_path = Path(self.project_path, "log")
        self.t = time.strftime("%Y_%m_%d")
        # self.format = "{time} {level} {module} {message}" 自定义日志格式,此处使用默认
        # print(self.project_path)

    def get_log(self, parent, level, msg):
        logger.remove()
        if not os.path.exists(f"{self.log_path}/{parent}"):
            os.makedirs(self.log_path / parent, 0o777)
        else:
            pass
        t = time.strftime("%Y_%m_%d")
        logger.add(f"{self.log_path}/{parent}/{t}.log", rotation=self.rotation,
                   encoding="utf-8", enqueue=self.enqueue,
                   retention=self.retention)

        if level == "INFO":
            return logger.info(msg)
        elif level == "warning":
            return logger.warning(msg)
        elif level == "DEBUG":
            return logger.debug(msg)
        elif level == "ERROR":
            return logger.error(msg)
        else:
            return logger.info(msg)


log = Logger()

if __name__ == '__main__':
    log.get_log("logging", "INFO", {'age': 3, 'name': 'zs'})
