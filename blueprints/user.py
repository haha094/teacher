from flask import Blueprint, request

from app import db
from utils import success, fail
from models import UserModel
from flask_cors import cross_origin

bp = Blueprint("user", __name__, url_prefix='/user')


@bp.post('/register')
@cross_origin()
def register():
    u = UserModel()
    param = request.get_json()
    # 如果工号uid已存在，查重
    uid = param.get('uid')
    user = UserModel.query.filter_by(uid=uid).first()
    if not uid:
        return fail("请确保工号已输入!")
    if user:
        return fail("该工号已注册!")
    else:
        u.uid = uid
        u.username = param.get('username')
        u.department_id = param.get('department_id')
        u.password = param.get('password')
        u.email = param.get('email')
        db.session.add(u)
        db.session.commit()
        return success("注册成功!")


@bp.post('/login')
@cross_origin()
def login():
    param = request.get_json()
    uid = param.get('uid')
    password = param.get('password')
    user = get_user_by_uid(uid)
    if not user:
        return fail("无此用户信息,请注册后重试!")
    else:
        if user.verify_password(password):
            # todo -- 是否生成token返回？
            return success("SUCCEED")
        else:
            return fail("工号或密码错误,请重试!")


@bp.get('/info/<uid>')
def get_user_info(uid):
    user = get_user_by_uid(uid)
    if user:
        data = user.to_dict()
        return success("SUCCEED", data)
    else:
        return fail("账户信息不存在!")


@bp.put('/pwd/update')
def update_password():
    param = request.get_json()
    uid = param.get('uid')
    old_password = param.get('oldPassword')
    new_password = param.get('newPassword')
    user = get_user_by_uid(uid)
    if not user:
        return fail("账户信息不存在!")
    else:
        if not user.verify_password(old_password):
            return fail("原密码错误，请重新输入!")
        else:
            user.password = new_password
            db.session.commit()
            return success("SUCCEED")


def get_user_by_uid(uid):
    return UserModel.query.filter_by(uid=uid).first()
