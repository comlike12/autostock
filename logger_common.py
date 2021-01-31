import logging
from logging.handlers import TimedRotatingFileHandler


class LoggerCommon:
    def __init__(self):
        # 로그 파일 핸들러
        self.fh_log = TimedRotatingFileHandler('C:/logs/log', when='midnight', encoding='utf-8', backupCount=120)
        self.fh_log.setLevel(logging.DEBUG)

        # 콘솔 핸들러
        self.sh = logging.StreamHandler()
        self.sh.setLevel(logging.DEBUG)

        # 로깅 포멧 설정
        self.formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
        self.fh_log.setFormatter(self.formatter)
        self.sh.setFormatter(self.formatter)

        # 로거 생성 및 핸들러 등록
        self.logger = logging.getLogger(__file__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.fh_log)
        self.logger.addHandler(self.sh)

    def get_logger_setting(self):
        return self.logger
