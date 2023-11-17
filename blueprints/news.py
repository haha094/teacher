import requests
from flask import Blueprint, request, render_template, jsonify
from flask_paginate import Pagination, get_page_args

from app import db
from utils import getNews, timeStampFormat, success, fail
from models import BriefNewsModel
from bs4 import BeautifulSoup

bp = Blueprint("news", __name__, url_prefix='/news')


def newsDataPack(brief_news, resourceData):
    contentData = resourceData['contentData']
    id = resourceData['id']
    news = BriefNewsModel.query.filter_by(id=id).first()
    if not news:
        brief_news.id = id
        brief_news.post_time = contentData['postTime']
        brief_news.cover = "".join(contentData['cover'])

        brief_news.brief = contentData['brief']
        brief_news.author_id = contentData['authorId']
        brief_news.author_name = contentData['authorName']
        brief_news.author_cover = contentData['authorCover']
        brief_news.author_home_page = contentData['authorHomePage']
        brief_news.title = contentData['title']
        brief_news.excerpt = contentData['excerpt']
        brief_news.url = 'https://www.sohu.com' + contentData['url']
        return brief_news
    else:
        return None


@bp.get("/index")
def render_index_html():
    if request.method == 'GET':
        return render_template("news_index.html")


@bp.get("/update")
def update_news():
    page = 1
    news_dict = getNews(page=page)
    count = news_dict['count']
    data = news_dict['data']
    brief_news_list = []
    for index in range(count):
        i_data = data[index]
        type_ = i_data['resourceType']
        brief_news = BriefNewsModel()
        resourceData = None
        if type_ == 1:
            resourceData = i_data['resourceData']
        else:
            resourceData = i_data['backupContent']['resourceData']
        # 封装数据
        brief_news = newsDataPack(brief_news, resourceData)
        # 插入列表中
        if brief_news:
            brief_news_list.append(brief_news)
    db.session.add_all(brief_news_list)
    db.session.commit()
    return success(message="NEWS UPDATE SUCCEED!!!")


@bp.route("/get_news_v1")
def get_news_v1():
    page_num = int(request.args.get('page_num'))
    per_size = int(request.args.get('page_size'))
    news_pagination_data = BriefNewsModel.query.paginate(page=page_num, per_page=per_size)
    # 当前页的数据列表
    brief_news_list = news_pagination_data.items
    for item in brief_news_list:
        item.post_time = timeStampFormat(int(item.post_time[:-3]))
    data = [news.to_dict() for news in brief_news_list]
    return success(message="SUCCEED!!!", data=data)


@bp.route("/get_news_v2")
def get_news_v2():
    page_num = int(request.args.get('page_num'))
    per_size = int(request.args.get('page_size'))
    news_pagination_data = BriefNewsModel.query.all()
    for item in news_pagination_data:
        item.post_time = int(item.post_time[:-3])
    sorted_list = sorted(news_pagination_data, key=lambda x: x.post_time, reverse=True)
    for item in sorted_list:
        item.post_time = timeStampFormat(item.post_time)
    '''
    1 20 => 0:20
    2 20 => 20:40
    3 20 => 40:60
    '''
    data = sorted_list[(page_num - 1) * per_size:page_num * per_size]
    data = [news.to_dict() for news in data]
    return success(message="SUCCEED!!!", data=data)


@bp.route("/get_total")
def get_total():
    brief_news_total = BriefNewsModel.query.count()
    return success(message="SUCCEED!!!", data=brief_news_total)


@bp.route("/detail")
def get_detail():
    brief_news_total = BriefNewsModel.query.count()
    return success(message="SUCCEED!!!", data=brief_news_total)


@bp.route("/detail/add")
def add_detail():
    # 指定要下载的页面的URL
    url = 'https://www.sohu.com/a/733225965_119038?scm=1101.topic:438647:110063.0.9.a2_3X771-0806_917'

    # 发送HTTP GET请求以获取页面内容
    response = requests.get(url)

    # 检查响应状态码
    if response.status_code == 200:
        # 获取页面内容
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find('article')
        # 将页面内容保存到本地文件
        # with open('page.html', 'w', encoding='utf-8') as file:
        #     file.write(html_content)
        article_text = article.get_text()
        print(f"HTML文件获取到的内容为：\n{article_text}")
    else:
        print('无法获取页面内容，HTTP响应状态码：', response.status_code)
    return success(message="SUCCEED!!!")
