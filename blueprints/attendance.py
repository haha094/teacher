from flask import Blueprint, request, jsonify

from app import db
from utils import success, fail

from workalendar.asia import China
from dateutil.rrule import rrule, WEEKLY
from datetime import datetime
from flask_cors import cross_origin

bp = Blueprint("attendance", __name__, url_prefix='/attendance')


@bp.get('/holidays')
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
