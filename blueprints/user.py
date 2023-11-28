from datetime import datetime, timedelta

from flask import Blueprint, request
from flask_cors import cross_origin

from app import db
from models import UserModel, UserTokenModel
from utils import success, fail, get_user_by_uid, get_user_by_token, loginErr, get_token_verificate_msg
from flask_jwt_extended import create_access_token

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
    # 用户信息不存在
    if not user:
        return fail("无此用户信息,请注册后重试!")
    # 密码错误，登录失败
    if not user.verify_password(password):
        return fail("工号或密码错误,请重试!")
    # 用户密码正确 => 登录成功
    token_str = create_access_token(identity=uid)
    # 该用户无token
    if not user.user_token_ref:
        user_token_model = UserTokenModel(uid=user.uid, token=token_str)
        db.session.add(user_token_model)
    # 有token =》 更新过期时间
    else:
        user_token = user.user_token_ref
        # 更新登录时间和过期时间
        user_token.login_time = datetime.now()
        user_token.expire_time = datetime.now() + timedelta(days=3)
        # token已过期 =》 更新token字符串
        if user_token.expire_time > datetime.now():
            user_token.token = token_str
    db.session.commit()
    return success("SUCCEED", data=token_str)


@bp.get('/info')
@cross_origin()
def get_user_info():
    token_str = request.headers.get('token')
    msg = get_token_verificate_msg(token_str)
    if not msg:
        return loginErr(msg)
    user = get_user_by_token(token_str)
    if not user:
        return fail("账户信息不存在!")
    data = user.to_dict()
    return success("SUCCEED", data)


@bp.put('/pwd/update')
@cross_origin()
def update_password():
    param = request.get_json()
    old_password = param.get('oldPassword')
    new_password = param.get('newPassword')
    token_str = request.headers.get('token')
    msg = get_token_verificate_msg(token_str)
    if not msg:
        return loginErr(msg)
    user = get_user_by_token(token_str)
    if not user:
        return fail("账户信息不存在!")
    if not user.verify_password(old_password):
        return fail("原密码错误，请重新输入!")
    user.password = new_password
    db.session.commit()
    return success("SUCCEED")
