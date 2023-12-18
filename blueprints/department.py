from flask import Blueprint, request,current_app

from utils import success, get_token_verificate_msg, loginErr
from models import DepartmentModel
from flask_cors import cross_origin

bp = Blueprint("department", __name__, url_prefix='/department')


@bp.get('/list')
@cross_origin()
def get_department_list():
    current_app.logger.info(f"{request.method} {request.path} request executed...")
    #token_str = request.headers.get('token')
    #msg = get_token_verificate_msg(token_str)
    #if not msg == 'OK':
    #    current_app.logger.error(f"{request.method} ERROR in {request.path} : {msg}")
    #    return loginErr(msg)
    departments = DepartmentModel.query.all()
    result = []
    for d in departments:
        result.append(d.to_dict())
    current_app.logger.info(f"The {request.method} {request.path} request has been successfully responded.")
    return success("SUCCEED", result)
