# mysql settings
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
