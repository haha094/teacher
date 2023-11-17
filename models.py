from extension import db
from utils import getTimeStamp


class BriefNewsModel(db.Model):
    __tablename__ = "brief_news"
    id = db.Column(db.Integer, primary_key=True)
    # 新闻发布时间的时间戳 * 1000
    post_time = db.Column(db.String(20))
    # 封面图片地址
    cover = db.Column(db.String(256))
    # 封面高度
    # cover_height = db.Column(db.Integer)
    # 封面宽度
    # cover_width = db.Column(db.Integer)
    # 新闻简要
    brief = db.Column(db.String(256))
    # 报社id
    author_id = db.Column(db.String(10))
    # 报社名
    author_name = db.Column(db.String(256))
    # 报社头像
    author_cover = db.Column(db.String(256))
    # 报社主页
    author_home_page = db.Column(db.String(256))

    # 标题
    title = db.Column(db.String(100))
    # 摘要
    excerpt = db.Column(db.Text)
    # 新闻详情url
    url = db.Column(db.String(256))

    def __str__(self):
        return f"{self.id}--{self.post_time}--{self.title}--{self.brief}--{self.url}"

    def to_dict(self):
        return {
            'id': self.id,
            'postTime': self.post_time,
            'cover': self.cover,
            'brief': self.brief,
            'authorId': self.author_id,
            'authorName': self.author_name,
            'author_cover': self.author_cover,
            'author_home_page': self.author_home_page,
            'title': self.title,
            'excerpt': self.excerpt,
            'url': self.url
        }

#
#     username = db.Column(db.String(100), nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     join_time = db.Column(db.DateTime, default=datetime.now)
