from datetime import datetime, timedelta

from extension import db
from werkzeug.security import generate_password_hash, check_password_hash
from shortuuid import uuid


class UserModel(db.Model):
    __tablename__ = "user"
    uid = db.Column(db.String(20), primary_key=True, comment='工号')
    username = db.Column(db.String(64), nullable=False, comment='用户名')
    password_hash = db.Column(db.String(128), comment='密码')
    email = db.Column(db.String(120), unique=True, nullable=False, comment='邮箱')

    # 定义用户与出勤信息的 一对多关系
    attendances = db.relationship("AttendanceModel", backref='user', lazy=True)

    # 外键 --》 部门与用户的一对多关系
    department_id = db.Column(db.String(20), db.ForeignKey('department.department_id'), nullable=False,
                              comment='部门编号')
    # 添加反向引用，表明是一个一对一关系
    user_token_ref = db.relationship("UserTokenModel", back_populates="user", uselist=False)

    def __str__(self):
        return f"{self.uid}--{self.username}--{self.department_id}--{self.email}"

    def to_dict(self):
        return {
            'uid': self.uid,
            'username': self.username,
            'department_id': self.department_id,
            'email': self.email
        }

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class DepartmentModel(db.Model):
    __tablename__ = "department"
    department_id = db.Column(db.String(20), primary_key=True, comment='部门编号')
    name = db.Column(db.String(64), nullable=False, comment='部门名')

    # 定义部门与用户的一对多关系
    users = db.relationship("UserModel", backref='department', lazy=True)

    def to_dict(self):
        return {
            'department_id': self.department_id,
            'name': self.name
        }


class AttendanceModel(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.String(50), primary_key=True, default=uuid, comment='出勤信息主键id')

    time = db.Column(db.String(20), nullable=False, comment='归属月份')
    work_cnt = db.Column(db.SmallInteger, nullable=False, comment='出勤天数')
    work_days = db.Column(db.Text, nullable=False, comment='出勤日期列表')
    memo = db.Column(db.Text, comment='备注信息')
    status = db.Column(db.Boolean, nullable=False, comment='出勤信息是否提交')
    department_id = db.Column(db.String(20), nullable=False, comment='归属部门编号')
    # 外键 --》 用户与出勤信息一对多
    uid = db.Column(db.String(20), db.ForeignKey('user.uid'), nullable=False, comment='归属用户id')

    def to_dict(self):
        return {
            'id': self.id,
            'time': self.time,
            'work_cnt': self.work_cnt,
            'work_days': self.work_days,
            'memo': self.memo,
            'status': self.status,
        }


class UserTokenModel(db.Model):
    __tablename__ = 'user_token'
    id = db.Column(db.String(50), primary_key=True, default=uuid)
    token = db.Column(db.String(512), unique=True, nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.now, comment='用户登录时间')
    expire_time = db.Column(db.DateTime, default=datetime.now() + timedelta(days=3), comment='token过期时间')
    # 外键 关联用户模型
    uid = db.Column(db.String(20), db.ForeignKey('user.uid'), nullable=False, comment='归属用户id')
    # 添加反向引用属性，表示一对一关系
    user = db.relationship("UserModel", back_populates="user_token_ref")

    def to_dict(self):
        return {
            'token': self.token,
            'create_time': self.create_time,
            'expire_time': self.expire_time,
        }
