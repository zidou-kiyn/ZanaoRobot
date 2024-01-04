import logging
import datetime

class Logger:
    def __init__(self, file_name):
        # 创建一个日志记录器
        self.logger = logging.getLogger(name=file_name)
        self.logger.setLevel(logging.INFO)

        # 设置日志输出格式
        formatter = logging.Formatter('[%(asctime)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # 创建一个文件处理器，用于写入日志文件，指定UTF-8编码
        file_handler = logging.FileHandler(file_name, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # 创建一个控制台处理器，用于输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, message):
        # 记录日志信息
        self.logger.info(message)
