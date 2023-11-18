from flask import Blueprint

from app import db
from utils import success, fail
from models import UserModel

bp = Blueprint("user", __name__, url_prefix='/user')

