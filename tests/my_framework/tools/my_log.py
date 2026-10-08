import logging
from pathlib import  Path
import time

# 路径
TODAY = time.strftime("%Y_%m_%d")
LOG_DIR = Path(__file__).resolve().parent.parent /"logs"


def create_logger(name:str= "XSHOP") ->logging.Logger:

    LOG_DIR.mkdir(parents=True,exist_ok=True)
    #创建对象
    logger = logging.getLogger(name)
    #防止重复创建
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    fmt = logging.Formatter(
        "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    #推送到控制台
    stream = logging.StreamHandler()
    #设置推送log展示格式
    stream.setFormatter(fmt)
    logger.addHandler(stream)

    #推送到本地文件
    file = logging.FileHandler(LOG_DIR / f"{TODAY}.log",encoding='utf-8')
    file.setFormatter(fmt)
    logger.addHandler(file)

    return logger

#作为全局默认配置,直接导入就可以用
log = create_logger()