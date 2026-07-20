import logging
import time
from pathlib import Path

#先定位路径
DATA_LOG = Path(__file__).resolve().parent.parent / "logs"
TODAY_DAY = time.strftime("%Y_%m_%d")

def get_logger(name="NEW_LOG"):
    DATA_LOG.mkdir(parents=True,exist_ok=True)
    logger = logging.getLogger(name)
    #每次都忘记
    if logger.handlers:
        return logger
    formatter = logging.Formatter('[%(asctime)s,%(msecs)03d] [%(levelname)s] [%(filename)s:%(lineno)d] ➡️ %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    logger.setLevel(logging.DEBUG)
    stream_log = logging.StreamHandler()
    stream_log.setFormatter(formatter)
    logger.addHandler(stream_log)

    #log_path_file = DATA_LOG / f"{TODAY_DAY}.log"
    # log_file = logging.FileHandler(log_path_file,encoding="utf-8")
    file_log = logging.FileHandler(DATA_LOG / '.log')
    file_log.setFormatter(formatter)
    logger.addHandler(file_log)



    return logger


if __name__ == '__main__':
    print(DATA_LOG)