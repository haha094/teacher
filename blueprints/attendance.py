import json

from flask import Blueprint, request

from app import db
from utils import success, fail, loginErr, get_user_by_token, get_token_verificate_msg, get_user_by_uid

from workalendar.asia import China
from dateutil.rrule import rrule, WEEKLY
from datetime import datetime
from flask_cors import cross_origin
from models import AttendanceModel, DepartmentModel
from sqlalchemy import and_

bp = Blueprint("attendance", __name__, url_prefix='/attendance')


@bp.get('/holidays')
@cross_origin()
def get_holidays():
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
    return success(message="SUCCEED", data=result)


@bp.post('/commit')
@cross_origin()
def commit_attendance():
    token_str = request.headers.get('token')
    msg = get_token_verificate_msg(token_str)
    if not msg:
        return loginErr(msg)
    user = get_user_by_token(token_str)
    if not user:
        return fail("该工号的用户信息已不存在!")
    attendance_model = AttendanceModel()
    attendance_model.uid = user.uid
    param = request.get_json()
    list = param.get('month_list')
    '''
    [{'time':'2023-10-21','remark':weekend},{'time':'2023-10-22','remark':'workday'},{},{},{}]
    '''
    # print(list)
    cnt = 0
    days = []
    memo = []
    for day in list:
        if day.get('remark') == 'workday':
            cnt += 1
            days.append({'time': day.get('time'), 'remark': day.get('remark')})
        else:
            memo.append({'time': day.get('time'), 'remark': day.get('remark')})
    attendance_model.work_days = json.dumps(days)
    attendance_model.memo = json.dumps(memo)
    attendance_model.work_cnt = cnt
    year = datetime.now().year
    month = datetime.now().month
    attendance_model.time = f"{year}-{month}"
    attendance_model.status = True
    attendance_model.department_id = user.department_id
    db.session.add(attendance_model)
    db.session.commit()
    return success("出勤信息提交成功!")


@bp.get('/list')
@cross_origin()
def get_attendance_list():
    token_str = request.headers.get('token')
    msg = get_token_verificate_msg(token_str)
    if not msg:
        return loginErr(msg)
    data = {}
    param = request.get_json()
    department_id = param.get('department_id')
    time = param.get('time')
    # print(f"time:{time},department_id:{department_id}")
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
    # print(department.users)
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


