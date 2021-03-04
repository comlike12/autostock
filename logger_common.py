# -*- coding: utf-8 -*-
import logging
from logging.handlers import TimedRotatingFileHandler


def createLogger(logger_name):
    # Create Logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Check handler exists
    if len(logger.handlers) > 0:
        return logger  # Logger already exists

    # 로그 파일 핸들러
    fh_log = TimedRotatingFileHandler('C:/logs/log', when='midnight', encoding='utf-8', backupCount=120)
    fh_log.setLevel(logging.DEBUG)

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
