from flask import Blueprint, request

from app import db
from utils import success, fail
from models import DepartmentModel
from flask_cors import cross_origin

bp = Blueprint("department", __name__, url_prefix='/department')


@bp.get('/list')
def get_department_list():
    departments = DepartmentModel.query.all()
    result = []
    for d in departments:
        result.append(d.to_dict())
    return success("SUCCEED", result)
