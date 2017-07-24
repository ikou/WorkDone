# -*- coding: utf-8 -*-
'''http接口实现'''
from __future__ import unicode_literals

import json
import time
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# workdone module
from WorkDone.service.login_ctrl import LoginService
from WorkDone.service.works_ctrl import WorksServices
from WorkDone.service.sch_ctrl import SchService


def index(request):
    '''根目录'''
    return render(request, 'index.html')


def my_dashboard(request):
    '''我的工作台'''
    return render(request, 'my_dashboard.html')


def leader_dashboard(request):
    '''领导展示页 展示部门整体情况'''
    return render(request, 'leader_dashboard.html')


def weekly_report(request):
    '''周报导出'''
    return render(request, 'weekly_report.html')


def admin_sync(request):
    '''测试用接口'''
    from WorkDone.dao.work_dao import WorksDAO
    WorksDAO.fix_status()

    return HttpResponse("ok")


def hello(request):
    '''测试用接口'''
    # from WorkDone.dao.work_dao import WorksDAO
    # WorksDAO.fix_status()

    return HttpResponse("ok")


def is_valid_date(datestr):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(datestr, "%Y-%m-%d")
        return 0
    except BaseException, e:
        return 1


def login(request):
    '''登录接口'''
    login_module = LoginService.get_instance()
    resp_json = {"error_code": None, "msg": None, "data": {}}

    # 获得用户名和密码
    user_name = request.GET.get('userName')
    user_password = request.GET.get('userPassword')
    if user_name and user_password:
        # 都不为空
        # 调用登录模块的login
        loginret = login_module.login(user_name, user_password)
        print loginret
        if loginret[0] == 1:
            # 登录成功
            resp_json["error_code"] = 0
            resp_json["msg"] = "login succ!"
            resp_json["data"]["token"] = loginret[2]
            return HttpResponse(json.dumps(resp_json))
        else:
            # 登录失败
            resp_json["error_code"] = 1
            resp_json["msg"] = "login fail!"
            return HttpResponse(json.dumps(resp_json))
    else:
        # 若有空值
        resp_json["error_code"] = 1
        resp_json["msg"] = "miss paramters!"
        return HttpResponse(json.dumps(resp_json))


def get_worklist(request):
    '''获得工作列表'''
    token = request.GET.get('token')
    status = request.GET.get('status')
    login_module = LoginService.get_instance()
    rest = login_module.check_token(token)
    work_module = WorksServices.get_instance()
    if rest[0] == 1:
        uid = rest[1]["user_id"]
        worklist = work_module.get_worklist(uid, status)
        return HttpResponse(json.dumps({"error_code": 0, "msg": "获取成功!",
                                        "data": {"works": worklist}}))
    else:
        return HttpResponse(json.dumps({"error_code": 1, "msg": "token error!", "data": {}}))


def get_work_by_id(request):
    '''根据id获得工作详情'''
    try:
        token = request.GET.get('token')
        workid = request.GET.get('id')
        login_module = LoginService.get_instance()
        rest = login_module.check_token(token)
        work_module = WorksServices.get_instance()
        if rest[0] == 1:
            # uid = rest[1]["user_id"]
            rest = work_module.get_workinfo(workid)
            return HttpResponse(json.dumps({"error_code": 0, "msg": "获取成功!",
                                            "data": rest}))
        else:
            return HttpResponse(json.dumps({"error_code": 1, "msg": "token error!", "data": {}}))

    except BaseException, e:
        print type(e)
        return HttpResponse(json.dumps({"error_code": 1, "msg": "exception error!", "data": {}}))


@csrf_exempt
def create_work(request):
    '''创建工作'''
    json_data = json.loads(request.body)
    try:
        token = json_data['token']
        summary = json_data['summary']
        start_date = json_data['StartDate']
        estimate_date = json_data['EstimateDate']
        if is_valid_date(start_date) == 1:
            return HttpResponse(json.dumps({"error_code": 1,
                                            "msg": "StartDate不是合法格式，请用Y-M-D格式", "data": {}}))
        #valid_status2 = is_valid_date(estimate_date)
        if is_valid_date(estimate_date) == 1:
            return HttpResponse(json.dumps({"error_code": 1,
                                            "msg": "EstimateDate不是合法格式，请用Y-M-D格式", "data": {}}))

        login_module = LoginService.get_instance()
        rest = login_module.check_token(token)
        if rest[0] == 1:
            uid = rest[1]["user_id"]
            work_module = WorksServices.get_instance()
            work_id = work_module.new_work(
                uid, summary, start_date, estimate_date)
            if work_id[0] == 0:
                return HttpResponse(json.dumps({"error_code": 0, "msg": "创建成功!",
                                                "data": {"id": work_id[1]}}))
            else:
                return HttpResponse(json.dumps({"error_code": 1, "msg": "创建异常!",
                                                "data": {}}))
        else:
            return HttpResponse(json.dumps({"error_code": 1, "msg": "token error!", "data": {}}))
    except BaseException, e:
        print type(e)
        return HttpResponse(json.dumps({"error_code": 1, "msg": "exception error!", "data": {}}))


@csrf_exempt
def update_work(request):
    '''更新工作内容'''
    json_data = json.loads(request.body)
    try:
        token = json_data['token']
        work_id = json_data['work_id']
        status = json_data['status']
        notes = json_data['Notes']
        reasons = json_data['Reasons']

        login_module = LoginService.get_instance()
        rest = login_module.check_token(token)

        if rest[0] == 1:
            work_module = WorksServices.get_instance()
            resp = work_module.update_work(work_id, status, notes, reasons)
            if resp == 0:
                return HttpResponse(json.dumps({"error_code": 0, "msg": "创建成功!",
                                                "data": {"id": work_id}}))
            else:
                return HttpResponse(json.dumps({"error_code": 1, "msg": "创建异常!",
                                                "data": {}}))
        else:
            return HttpResponse(json.dumps({"error_code": 1, "msg": "token error!", "data": {}}))
    except BaseException, e:
        print type(e)
        return HttpResponse(json.dumps({"error_code": 1, "msg": "exception error!", "data": {}}))


def query_issuelist_v2(request):
    '''获得所有员工异常工作列表'''
    try:
        token = request.GET.get('token')
        login_module = LoginService.get_instance()
        rest = login_module.check_token(token)
        work_module = WorksServices.get_instance()
        if rest[0] == 1:
            rest = work_module.get_issuework_v2()
            return HttpResponse(json.dumps({"error_code": 0, "msg": "获取成功!",
                                            "data": rest}))
        else:
            return HttpResponse(json.dumps({"error_code": 1, "msg": "token error!", "data": {}}))

    except BaseException, e:
        print type(e)
        return HttpResponse(json.dumps({"error_code": 1, "msg": "exception error!", "data": {}}))



def query_issuelist(request):
    '''获得所有员工异常工作列表'''
    try:
        token = request.GET.get('token')
        login_module = LoginService.get_instance()
        rest = login_module.check_token(token)
        work_module = WorksServices.get_instance()
        if rest[0] == 1:
            rest = work_module.get_issuework()
            return HttpResponse(json.dumps({"error_code": 0, "msg": "获取成功!",
                                            "data": rest}))
        else:
            return HttpResponse(json.dumps({"error_code": 1, "msg": "token error!", "data": {}}))

    except BaseException, e:
        print type(e)
        return HttpResponse(json.dumps({"error_code": 1, "msg": "exception error!", "data": {}}))


def get_weeklyreport(request):
    '''获得所有员工异常工作列表'''
    try:
        token = request.GET.get('token')
        day = request.GET.get('day')
        login_module = LoginService.get_instance()
        rest = login_module.check_token(token)
        work_module = WorksServices.get_instance()
        if rest[0] == 1:
            rest = work_module.export(day)
            return HttpResponse(json.dumps({"error_code": 0, "msg": "获取成功!",
                                            "data": rest}))
        else:
            return HttpResponse(json.dumps({"error_code": 1, "msg": "token error!", "data": {}}))

    except BaseException, e:
        print type(e)
        return HttpResponse(json.dumps({"error_code": 1, "msg": "exception error!", "data": {}}))


def get_self_weeklyreport(request):
    '''获得自己的工作周报'''
    try:
        token = request.GET.get('token')
        day = request.GET.get('day')
        login_module = LoginService.get_instance()
        rest = login_module.check_token(token)
        work_module = WorksServices.get_instance()
        if rest[0] == 1:
            uid = rest[1]["user_id"]
            rest = work_module.export_self(uid, day)

            return HttpResponse(json.dumps({"error_code": 0, "msg": "获取成功!",
                                            "data": rest[1]}))
        else:
            return HttpResponse(json.dumps({"error_code": 1, "msg": "token error!", "data": {}}))

    except BaseException, e:
        print type(e)
        return HttpResponse(json.dumps({"error_code": 1, "msg": "exception error!", "data": {}}))


login_module = SchService.get_instance()
login_module.start_sch()
