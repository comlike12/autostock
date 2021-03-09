# -*- coding: utf-8 -*-
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def createLogger(logger_name):
    # Create Logger
    logger = logging.getLogger(logger_name)

    # Check handler exists
    if len(logger.handlers) > 0:
        return logger  # Logger already exists

    logger.setLevel(logging.DEBUG)

    # 로그 파일 핸들러
    nowDay = datetime.today().strftime("%Y%m%d")
    logfilepath = f"C:/logs/{nowDay}.log"
    fh_log = TimedRotatingFileHandler(logfilepath, when='midnight', encoding='utf-8', backupCount=120)
    # 콘솔 핸들러
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(levelname)s|%(name)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
    fh_log.setFormatter(formatter)
    sh.setFormatter(formatter)

    # Create Handlers
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)

    # logger.addHandler(streamHandler)
    logger.addHandler(fh_log)
    logger.addHandler(sh)

    return logger
