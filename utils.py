import time
from datetime import date, datetime
from flask import current_app
from models import UserModel, UserTokenModel

import secrets
import string
from flask import jsonify


# 返回日志打印时的时间信息
def nowDateTime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_user_by_uid(uid):
    return UserModel.query.filter_by(uid=uid).first()


def get_user_by_token(token_str):
    user_token = UserTokenModel.query.filter_by(token=token_str).first()
    if not user_token:
        return None
    else:
        return user_token.user


def generateResult(code, msg, data):
    return jsonify({
        'code': code,
        'msg': msg or "",
        'data': data or {}
    })


# 生成一个强密码
def generate_secure_key(length=5):
    characters = string.ascii_letters + string.digits + string.punctuation
    secure_key = ''.join(secrets.choice(characters) for i in range(length))
    return secure_key


# 响应成功
def success(message=None, data=None):
    return generateResult(
        code=200,
        msg=message,
        data=data
    )


# 响应失败
def fail(message=None, data=None):
    return generateResult(
        code=500,
        msg=message,
        data=data
    )


def loginErr(message=None):
    return generateResult(
        code=401,
        msg=message,
        data=None
    )


def get_token_verificate_msg(token_str):
    # 无token字符串传入 => 未登录
    if not token_str:
        return "请登录后重试!"
    # 根据token查找用户token信息
    user_token = UserTokenModel.query.filter_by(token=token_str).first()

    # 用户token信息存在
    if user_token:
        # 用户token信息已过期
        now = datetime.now()
        # current_app.logger.debug(f"user_token.expire_time?{user_token.expire_time}")
        # current_app.logger.debug(f"now > user_token.expire_time?{now > user_token.expire_time}")
        if now > user_token.expire_time:
            return "用户信息已过期,请重新登录!"
        # 用户token未过期
        else:
            return "OK"
    # 用户token信息不存在
    else:
        return "请登录后重试!"
