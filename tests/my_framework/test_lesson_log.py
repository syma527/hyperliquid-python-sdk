import logging
import time
from pathlib import Path

TODAY = time.strftime("%Y_%m_%d")
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"


def create_logger(name: str = "MY_FRAMEWORK") -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:          # 防重复！同名 logger 是全局单例，重复 addHandler 会打多遍
        return logger

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter(
        "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream = logging.StreamHandler()          # 通道1：给人眼实时看
    stream.setFormatter(fmt)
    logger.addHandler(stream)

    file = logging.FileHandler(LOG_DIR / f"{TODAY}.log", encoding="utf-8")   # 通道2：给事后查
    file.setFormatter(fmt)
    logger.addHandler(file)

    return logger


log = create_logger()