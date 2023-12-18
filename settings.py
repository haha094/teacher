import os
import logging
import time
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from datetime import timedelta

from utils import generate_secure_key


class MySqlConfig(object):
    DEBUG = True
    # SECRET_KEY = "ltx_secret_key"  # session的啥东西
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql//{}:{}@{}:{}/{}" \
    #     .format(username="root", password="071428", host="127.0.0.1", port=3306, database="mall")
    # windows主机
    # HOSTNAME = "127.0.0.1"
    # PORT = 3306
    # USERNAME = "root"
    # PASSWORD = "071428"
    # DATABASE = "teacher_attendance_system"

    # Ubuntu虚拟机
    HOSTNAME = "10.21.150.132"
    PORT = 3306
    USERNAME = "ltx"
    PASSWORD = "123456"
    DATABASE = "teacher_attendance_system"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT,
                                                                                   DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 动态追踪拦截
    SQLALCHEMY_ECHO = True  # 日志级别：显示sql语句
    # SQLALCHEMY_ECHO = False  # 日志级别：显示sql语句
    # SQLALCHEMY_ECHO = logging.DEBUG  # 日志级别显示sql语句


# WHITE_NAME_LIST = ["/api/login","/api/regist","/api/goods/type","/api/by/tag/goods"]

class JwtConfig(object):
    # 设置token过期时间为48小时后
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=48)
    # 将秘钥更改为强密码
    JWT_SECRET_KEY = generate_secure_key()


# class LoggingConfig:
#     # 日志级别，默认为 INFO
#     # LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
#     LOG_LEVEL_ERR = logging.ERROR
#     LOG_LEVEL_INFO = logging.INFO
#     LOG_LEVEL_DEBUG = logging.DEBUG
#
#     # 日志文件存储目录，默认为 "logs"
#     LOG_DIR = os.environ.get('LOG_DIR', 'logs')
#     # 定义日志文件的完整路径
#     LOG_FILE_ERROR = os.path.join(LOG_DIR, 'error.log')
#     LOG_FILE_INFO = os.path.join(LOG_DIR, 'info.log')
#     LOG_FILE_DEBUG = os.path.join(LOG_DIR, 'debug.log')
#
#     LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
#     LOG_FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=LOG_DATE_FORMAT)
#     LOG_MAX_BYTES = 100000
#     LOG_BACKUP_COUNT = 10
#
#     @classmethod
#     def init_app(cls, app):
#         # 添加ERROR 级别的日志处理器
#         error_file_handler = RotatingFileHandler(cls.LOG_FILE_ERROR, maxBytes=cls.LOG_MAX_BYTES,
#                                                  backupCount=cls.LOG_BACKUP_COUNT, encoding='utf-8')
#         error_file_handler.setLevel(cls.LOG_LEVEL_ERR)
#         error_file_handler.setFormatter(cls.LOG_FORMAT)
#         app.logger.addHandler(error_file_handler)
#
#         # 添加 INFO 级别的日志处理器
#         # info_file_handler = RotatingFileHandler(cls.LOG_FILE_INFO, maxBytes=cls.LOG_MAX_BYTES,
#         #                                         backupCount=cls.LOG_BACKUP_COUNT, encoding='utf-8')
#         # info_file_handler.setLevel(cls.LOG_LEVEL_INFO)
#         # info_file_handler.setFormatter(cls.LOG_FORMAT)
#         # app.logger.addHandler(info_file_handler)
#
#         # 添加 DEBUG 级别的日志处理器
#         debug_file_handler = RotatingFileHandler(cls.LOG_FILE_DEBUG, maxBytes=cls.LOG_MAX_BYTES,
#                                                  backupCount=cls.LOG_BACKUP_COUNT, encoding='utf-8')
#         debug_file_handler.setLevel(cls.LOG_LEVEL_DEBUG)
#         debug_file_handler.setFormatter(cls.LOG_FORMAT)
#         app.logger.addHandler(debug_file_handler)


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
    LOG_FILE_DB = os.path.join(LOG_DIR, 'database.log')

    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOG_FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=LOG_DATE_FORMAT)
    LOG_MAX_BYTES = 100000
    LOG_BACKUP_COUNT = 10

    @classmethod
    def init_app(cls, app):
        # 自动删除过期日志
        LOG_DIR = os.environ.get('LOG_DIR', 'logs')
        max_age_days = 30
        current_time = time.time()
        max_age_seconds = max_age_days * 86400
        for filename in os.listdir(LOG_DIR):
            file_path = os.path.join(LOG_DIR, filename)
            file_stat = os.stat(file_path)

            # 检查文件最后修改时间是否超过最大年龄
            if current_time - file_stat.st_mtime > max_age_seconds:
                try:
                    os.remove(file_path)
                    print(f"Deleted old log file: {filename}")
                except Exception as e:
                    print(f"Error deleting file {filename}: {e}")

        # 时间轮转日志处理器 - ERROR 级别
        error_file_handler = TimedRotatingFileHandler(cls.LOG_FILE_ERROR, when='D', interval=1, backupCount=1440,
                                                      encoding='utf-8')
        error_file_handler.setLevel(cls.LOG_LEVEL_ERR)
        error_file_handler.setFormatter(cls.LOG_FORMAT)
        app.logger.addHandler(error_file_handler)

        # 时间轮转日志处理器 - DEBUG 级别
        debug_file_handler = TimedRotatingFileHandler(cls.LOG_FILE_DEBUG, when='D', interval=1, backupCount=1440,
                                                      encoding='utf-8')
        debug_file_handler.setLevel(cls.LOG_LEVEL_DEBUG)
        debug_file_handler.setFormatter(cls.LOG_FORMAT)
        app.logger.addHandler(debug_file_handler)

        # 设置日志记录器
        sql_handler = RotatingFileHandler('sqlalchemy.log', maxBytes=10000, backupCount=1)
        sql_handler.setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.engine').addHandler(sql_handler)

