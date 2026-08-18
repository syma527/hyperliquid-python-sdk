import logging
import time
from pathlib import Path

#切分文件的名字
TODAY_DATE = time.strftime("%Y_%m_%d")
LOG_DIR =  Path(__file__).resolve().parent.parent /"logs"
#如果不存在自动创建


def create_logger(name="XSHOP"):
    #创建文件这个功能好用
    LOG_DIR.mkdir(parents=True,exist_ok=True)
    #首先要去logging新建实例
    logger = logging.getLogger(name)
    #这个判断很重要,防止重复日志输出
    if logger.handlers:
        return logger
    #设置不同信息等级,放到下面
    logger.setLevel(logging.INFO)
    #格式化输出日志格式
    log_format = logging.Formatter(
        '[%(asctime)s,%(msecs)03d] [%(levelname)s] [%(filename)s:%(lineno)d] ➡️ %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    #输出到控制台
    #Handler 创建三步走： 一建、二设、三添加 分开写，更清晰 调试修改都容易
    log_stream = logging.StreamHandler()
    log_stream.setFormatter(log_format)
    logger.addHandler(log_stream)
    #保存到本地
    log_file_path = LOG_DIR / f"{TODAY_DATE}.log"
    log_file = logging.FileHandler(log_file_path,encoding="utf-8")
    log_file.setFormatter(log_format)
    logger.addHandler(log_file)
    return logger


