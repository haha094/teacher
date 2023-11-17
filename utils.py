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


# save data as file
def down_data(page, content):
    with open('搜狐时政_' + str(page) + '.json', 'w', encoding='utf-8') as fp:
        fp.write(content)


def getNews(page):
    url = 'https://cis.sohu.com/cisv4/feeds'
    # url = "https://cis.sohu.com/cisv3/feeds"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        "Cookie": "gidinf=x099980109ee1753ad15e1858000784d6b0cd49b1d1e; SUV=230717174934U5QG; IPLOC=CN; clt=1696685476; cld=20231007213116; reqtype=pc; t=1696685493506",
        "Content-Type": "application/json;charset=utf-8"
    }
    param = {
        'clientType': 3,
        'pvId': '1696675166609_Rv9TnyW',
        'resourceParam': [
            {
                "requestId": "1696686686702_23071717493_Nt2",
                'resourceId': '1001563447688888320',
                'page': page,
                'size': 270,
                'spm': 'smpc.channel_114.block3_77_O0F7zf_1_fd',
                'context': {
                    'feedType': "XTOPIC_SYNTHETICAL",
                    'pro': '0,1'
                },
                'productParam': {
                    'productId': 438647,
                    'productType': 15,
                    'categoryId': 47,
                    'mediaId': 1
                },
                'resProductParam': {
                    'adTags': '20000111',
                    'productId': 1523,
                    'productType': 13
                },
                'expParam': {},
            }
        ],
        'suv': '1690177869726ceuoqp'
    }
    # post请求的参数 必须要进行编码
    param = json.dumps(param).encode('utf-8')
    requ = urllib.request.Request(url=url, data=param, headers=headers)
    # 模拟浏览器向服务器发送请求
    response = urllib.request.urlopen(requ)
    # return response
    # 获取响应的数据
    content = response.read().decode('utf-8')
    # return content
    # 将获取到的json字符串转成字典返回
    json_loads = json.loads(content)
    dic = json_loads['1001563447688888320']
    # print(dic)
    # print(type(dic))
    return dic


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
