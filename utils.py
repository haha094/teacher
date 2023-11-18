import time
from datetime import date

import simplejson as json
import urllib.request
import urllib.parse

import json

from flask import jsonify


# get current time stamp
def getTimeStamp():
    return time.localtime()


# timeStamp to data
def timeStampFormat(timeStamp):
    return date.fromtimestamp(timeStamp).strftime("%Y.%m.%d")


def generateResult(code, msg, data):
    return jsonify({
        'code': code,
        'msg': msg or "",
        'data': data or {}
    })


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
