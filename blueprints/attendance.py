import json

from flask import Blueprint, request, current_app
import requests
from extension import db
from utils import success, fail, loginErr, get_user_by_token, get_token_verificate_msg, get_user_by_uid

from workalendar.asia import China
from dateutil.rrule import rrule, WEEKLY
from datetime import datetime
from flask_cors import cross_origin
from models import AttendanceModel, DepartmentModel
from sqlalchemy import and_

bp = Blueprint("attendance", __name__, url_prefix='/attendance')


@bp.get('/abandon/holidays')
@cross_origin()
def get_holidays_abandon():
    current_app.logger.info(f"{request.method} {request.path} request executed...")
    year = datetime.now().year
    month = datetime.now().month
    cal = China()
    holidays = cal.holidays(year)
    weekend = find_weekends(year)
    for weekend_day in weekend:
        # 若周末那天已存在于节假日列表中，则该天不算周末，不重复添加到holidays列表中
        if not date_exists(weekend_day, holidays):
            weekend_date = (weekend_day, 'weekend')
            holidays.append(weekend_date)
    # todo：因为没有找到第三方库能把调休上班的周末筛选出来，因此哪怕2023.10.7和2023.10.8需要上班，也在holidays列表中
    # todo：！！！因此！！！ 用户需要在前端手动出勤10.7和10.8
    # 返回当月month的节假日列表
    result = []
    for holiday in holidays:
        flag = month == holiday[0].month
        if flag:
            result.append({"time": holiday[0].strftime('%Y-%m-%d'), "remark": holiday[1]})
    # print(f"返回当月的节假日列表result={result}")
    current_app.logger.info(f"The {request.method} {request.path} request has been successfully responded.")
    return success(message="SUCCEED", data=result)


@bp.get('/holidays')
@cross_origin()
def get_holidays():
    current_app.logger.info(f"{request.method} {request.path} request executed...")
    # year = datetime.now().year
    # month = datetime.now().month

    param = request.get_json()
    year = int(param.get('year'))
    month = int(param.get('month'))

    url = "https://www.mxnzp.com/api/holiday/list/month/{}{:02d}?ignoreHoliday=false&app_id=ridopeqfimyqpyrh&app_secret=18DaFPw83fxCWE2TB9gvnCEtLRXHcQoN".format(
        year, month)

    response = requests.get(url)
    # 直接获取 JSON 数据
    holidays_data = response.json()

    holidays_list = holidays_data.get('data', [])

    result = []
    for hd in holidays_list:
        if hd['typeDes'] != '工作日':
            result.append({"time": hd['date'], "remark": hd['typeDes']})
    current_app.logger.info(f"The {request.method} {request.path} request has been successfully responded.")
    return success(message="SUCCEED", data=result)

# {"time": "2023-12-1", "remark": "workday"}, {"time": "2023-12-4", "remark": "workday"}, {"time": "2023-12-5", "remark": "workday"}, {"time": "2023-12-6", "remark": "workday"}, {"time": "2023-12-7", "remark": "workday"}, {"time": "2023-12-8", "remark": "workday"}, {"time": "2023-12-11", "remark": "workday"}, {"time": "2023-12-12", "remark": "workday"}, {"time": "2023-12-13", "remark": "workday"}, {"time": "2023-12-14", "remark": "workday"}, {"time": "2023-12-15", "remark": "workday"}, {"time": "2023-12-18", "remark": "workday"}, {"time": "2023-12-19", "remark": "workday"}, {"time": "2023-12-20", "remark": "workday"}, {"time": "2023-12-21", "remark": "workday"}, {"time": "2023-12-22", "remark": "workday"}, {"time": "2023-12-25", "remark": "workday"}, {"time": "2023-12-26", "remark": "workday"}, {"time": "2023-12-27", "remark": "workday"}, {"time": "2023-12-28", "remark": "workday"}, {"time": "2023-12-29", "remark": "workday"}
@bp.post('/commit')
@cross_origin()
def commit_attendance():
    current_app.logger.info(f"{request.method} {request.path} request executed...")
    token_str = request.headers.get('token')
    msg = get_token_verificate_msg(token_str)
    if not msg == "OK":
        current_app.logger.error(f"{request.method} ERROR in {request.path} : {msg}")
        return loginErr(msg)
    user = get_user_by_token(token_str)
    if not user:
        msg = "该工号的用户信息已不存在!"
        current_app.logger.error(f"{request.method} ERROR in {request.path} : {msg}")
        return fail(msg)
    attendance_model = AttendanceModel()
    attendance_model.uid = user.uid
    department_id = user.department_id
    param = request.get_json()
    month_list = param.get('month_list')
    year = month_list[0].get('time').split('-')[0]
    month = month_list[0].get('time').split('-')[1]
    time = f"{year}-{month}"
    attendance_model.time = time
    # 若该用户已提交，此次提交不成功
    attendance_exit = AttendanceModel.query.filter(and_(AttendanceModel.uid == user.uid, AttendanceModel.time == time)).first()
    if attendance_exit:
        return fail(message="您已提交该月的出勤信息")
    cnt = 0
    days = []
    memo = []
    for day in month_list:
        if day.get('remark') == 'workday':
            cnt += 1
            days.append({'time': day.get('time'), 'remark': day.get('remark')})
        else:
            memo.append({'time': day.get('time'), 'remark': day.get('remark')})
    attendance_model.work_days = json.dumps(days)
    attendance_model.memo = json.dumps(memo)
    attendance_model.work_cnt = cnt

    attendance_model.status = True
    attendance_model.department_id = department_id
    db.session.add(attendance_model)
    db.session.commit()
    current_app.logger.info(f"The {request.method} {request.path} request has been successfully responded.")
    return success("出勤信息提交成功!")


@bp.post('/list')
@cross_origin()
def get_attendance_list():
    current_app.logger.info(f"{request.method} {request.path} request executed...")
    token_str = request.headers.get('token')
    msg = get_token_verificate_msg(token_str)
    if not msg == 'OK':
        current_app.logger.error(f"{request.method} ERROR in {request.path} : {msg}")
        return loginErr(msg)
    data = {}
    param = request.get_json()
    department_id = param.get('department_id')
    time = param.get('time')
    commited_list = []
    data["department_id"] = department_id
    list = AttendanceModel.query.filter(
        and_(AttendanceModel.department_id == department_id, AttendanceModel.time == time)).all()
    # 已提交用户
    temp = []
    for i in list:
        if i.status:
            user = get_user_by_uid(i.uid)
            if not user:
                current_app.logger.error(f"{request.method} ERROR in {request.path} : 该工号的用户信息已不存在!")
                return fail("该工号的用户信息已不存在!")
            else:
                commited_list.append({
                    'uid': user.uid,
                    'name': user.username,
                    'days': i.work_cnt,
                    'workingDays': json.loads(i.work_days),
                    'holidays': json.loads(i.memo)
                })
                temp.append(user)
    data["commitedList"] = commited_list
    # 未提交用户 ---》 添加用户名、工号
    uncommited_list = []
    department = DepartmentModel.query.filter_by(department_id=department_id).first()

    temp_uids = [user.uid for user in temp]
    # department.users 中排除 temp 中的用户
    uncommited_users = [user for user in department.users if user.uid not in temp_uids]
    # print(uncommited_users)
    for item in uncommited_users:
        uncommited_list.append({
            'uid': item.uid,
            'name': item.username,
            'days': 0
        })
    data['uncommitedList'] = uncommited_list
    current_app.logger.info(f"The {request.method} {request.path} request has been successfully responded.")
    return success("SUCCEED", data)


def find_weekends(year):
    # 开始日期和结束日期
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    # 使用 rrule 查找周六和周日
    weekends = list(rrule(freq=WEEKLY, dtstart=start_date, until=end_date, byweekday=(5, 6)))
    return [day.date() for day in weekends]


def date_exists(check_date, lst):
    for d, _ in lst:
        if d == check_date:
            return True
    return False


@bp.get('/haha/test')
def example():
    current_path = request.path
    request_url = request.url
    print(f"request_url={request_url}")
    print(f"current_path={current_path}")
    return "hahaha test"
