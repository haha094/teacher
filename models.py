from extension import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    __tablename__ = "user"
    uid = db.Column(db.String(20), primary_key=True, comment='工号')
    username = db.Column(db.String(64), nullable=False, comment='用户名')
    department_id = db.Column(db.String(20), nullable=False, comment='部门编号')
    password_hash = db.Column(db.String(128), comment='密码')
    email = db.Column(db.String(120), unique=True, nullable=False, comment='邮箱')

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
