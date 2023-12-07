import os
import logging
from logging.handlers import RotatingFileHandler

from datetime import timedelta

from utils import generate_secure_key


class MySqlConfig(object):
    DEBUG = True
    # SECRET_KEY = "ltx_secret_key"  # session的啥东西
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql//{}:{}@{}:{}/{}" \
    #     .format(username="root", password="071428", host="127.0.0.1", port=3306, database="mall")
    HOSTNAME = "127.0.0.1"
    PORT = 3306
    USERNAME = "root"
    PASSWORD = "071428"
    DATABASE = "teacher_attendance_system"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT,
                                                                                   DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 动态追踪拦截
    # SQLALCHEMY_ECHO = True  # 日志级别：显示sql语句
    SQLALCHEMY_ECHO = False  # 日志级别：显示sql语句
    # SQLALCHEMY_ECHO = logging.ERROR  # 日志级别显示sql语句


# WHITE_NAME_LIST = ["/api/login","/api/regist","/api/goods/type","/api/by/tag/goods"]

class JwtConfig(object):
    # 设置token过期时间为48小时后
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=48)
    # 将秘钥更改为强密码
    JWT_SECRET_KEY = generate_secure_key()


class LoggingConfig:
    # 日志级别，默认为 INFO
    # LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_LEVEL_ERR = logging.ERROR
    LOG_LEVEL_INFO = logging.INFO
    LOG_LEVEL_DEBUG = logging.DEBUG

    # 日志文件存储目录，默认为 "logs"
    LOG_DIR = os.environ.get('LOG_DIR', 'logs')
    # 定义日志文件的完整路径
    LOG_FILE_ERROR = os.path.join(LOG_DIR, 'error.log')
    LOG_FILE_INFO = os.path.join(LOG_DIR, 'info.log')
    LOG_FILE_DEBUG = os.path.join(LOG_DIR, 'debug.log')

    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOG_FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=LOG_DATE_FORMAT)
    LOG_MAX_BYTES = 100000
    LOG_BACKUP_COUNT = 10

    @classmethod
    def init_app(cls, app):
        # 添加ERROR 级别的日志处理器
        error_file_handler = RotatingFileHandler(cls.LOG_FILE_ERROR, maxBytes=cls.LOG_MAX_BYTES,
                                                 backupCount=cls.LOG_BACKUP_COUNT, encoding='utf-8')
        error_file_handler.setLevel(cls.LOG_LEVEL_ERR)
        error_file_handler.setFormatter(cls.LOG_FORMAT)
        app.logger.addHandler(error_file_handler)

        # 添加 INFO 级别的日志处理器
        # info_file_handler = RotatingFileHandler(cls.LOG_FILE_INFO, maxBytes=cls.LOG_MAX_BYTES,
        #                                         backupCount=cls.LOG_BACKUP_COUNT, encoding='utf-8')
        # info_file_handler.setLevel(cls.LOG_LEVEL_INFO)
        # info_file_handler.setFormatter(cls.LOG_FORMAT)
        # app.logger.addHandler(info_file_handler)

        # 添加 DEBUG 级别的日志处理器
        debug_file_handler = RotatingFileHandler(cls.LOG_FILE_DEBUG, maxBytes=cls.LOG_MAX_BYTES,
                                                 backupCount=cls.LOG_BACKUP_COUNT, encoding='utf-8')
        debug_file_handler.setLevel(cls.LOG_LEVEL_DEBUG)
        debug_file_handler.setFormatter(cls.LOG_FORMAT)
        app.logger.addHandler(debug_file_handler)
