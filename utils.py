import time
from datetime import date, datetime

import simplejson as json
import urllib.request
import urllib.parse
from models import UserModel, UserTokenModel

import json
import secrets
import string
from flask import jsonify


# get current time stamp
def getTimeStamp():
    return time.localtime()


# timeStamp to data
def timeStampFormat(timeStamp):
    return date.fromtimestamp(timeStamp).strftime("%Y.%m.%d")


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


def ReLogin():
    return generateResult(
        code=401,
        msg="令牌已过期,请重新登录!",
        data=None
    )


def is_token_expired(token_str):
    user_token = UserTokenModel.query.filter_by(token=token_str).first()
    if user_token:
        now = datetime.now()
        return now > user_token.expire_time
    else:
        return False





