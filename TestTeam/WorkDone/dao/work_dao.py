# -*- coding: utf-8 -*-

import datetime
import time

import sys
import os
import shutil

from tempfile import TemporaryFile
from xlwt import Workbook

from WorkDone.my_models.works_model import worksDTO
from WorkDone.my_models.worksRelation_model import worksRelationDTO
from WorkDone.my_models.auth_model import Auth

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WorksDAO(object):
    def __init__(self):
        self.works = None

    def new_work(self, uid, summary, StartDate, EstimateDate):
        '''Create a work data'''
        try:
            self.works = worksDTO()
            self.works.summary = summary
            self.works.StartDate = StartDate
            self.works.EstimateDate = EstimateDate

            start_date_t = time.strptime(StartDate, "%Y-%m-%d")
            today = time.localtime(time.time())
            # print "step2"
            if start_date_t > today:
                status = "todo"
            else:
                status = "ongoing"
            self.works.Status = status

            self.works.save()
            work_id = self.works.id
            del self.works

            self.new_relationWork(work_id, uid, status)

            return 0, work_id
        except BaseException, e:
            print type(e)
            return 1, "error"

    def new_relationWork(self, wid, uid, status):
        '''Create a relation work data'''
        print wid
        print uid
        print status
        relatonWorks = worksRelationDTO()
        relatonWorks.user_id = uid
        relatonWorks.work_id = wid
        relatonWorks.work_status = status
        relatonWorks.save()
        del relatonWorks

    def update_releationWork(self, wid, status):
        '''Create a relation work data'''
        relatonWorks = worksRelationDTO.objects.get(work_id=wid)
        relatonWorks.work_status = status
        relatonWorks.save()
        del relatonWorks

    def update_work(self, work_id, status=None, Notes=None, Reasons=None):
        '''Update a work data'''
        try:
            upwork = worksDTO.objects.get(id=work_id)
            upwork.Status = status
            upwork.Notes = Notes
            if status == "done":
                now = datetime.datetime.now()
                now_str = now.strftime('%Y-%m-%d')  
                upwork.DoneDate = now_str
            # if Reasons != None:
            #     if len(Reasons) > 10:
            #         print "*ERROR* The Reasons is larger than 10."
            #     string_Reasons = ','.join(Reasons)
            #     upwork.Reasons = string_Reasons
            # else:
            upwork.Reasons = Reasons
            upwork.save()
            del upwork
            self.update_releationWork(work_id, status)
            return 0
        except BaseException, e:
            return 1

    def getWorkList(self, uid, status=None):
        '''Get personal work list'''
        try:
            worklist = []
            if status == None:
                getworks = worksRelationDTO.objects.filter(user_id=uid)
                for obwork in getworks:
                    worklist.append(obwork.work_id)
            else:
                getworks = worksRelationDTO.objects.filter(
                    user_id=uid, status=status)
                for obwork in getworks:
                    worklist.append(obwork.work_id)
            return worklist
        except BaseException, e:
            print e

    def getWorkInfo(self, work_id):
        '''Get one work detailed info'''
        try:
            #Reasons = []
            work = worksDTO.objects.get(id=work_id)
            summary = work.summary
            StartDate = work.StartDate
            EstimateDate = work.EstimateDate
            DoneDate = work.DoneDate
            Status = work.Status
            Notes = work.Notes
            Reasons = work.Reasons
            # print work.Reasons
            # try:
            #     Reasons = work.Reasons.split(',')
            # except BaseException, e:
            #     Reasons = []
            #     print type(e)
            data = {
                "id": work_id,
                "summary": summary,
                "StartDate": StartDate,
                "EstimateDate": EstimateDate,
                "DoneDate": DoneDate,
                "Status": Status,
                "Notes": Notes,
                "Reason": Reasons
            }
            return data
        except BaseException, e:
            print e




    def getIssueWork_v2(self):
        '''Get all user_id from worksRelationDTO'''
        try:
            data = {}
            userid_list = worksRelationDTO.objects.values_list(
                'user_id', flat=True)
            user_list = list(set(userid_list))
            for uid in user_list:
                udict = {}
                auth_obj = Auth.objects.get(userid=uid)
                username = auth_obj.username
                mail = auth_obj.name
                delay_worklist = []
                pending_worklist = []
                ongoing_worklist = []
                ongoingWork = worksRelationDTO.objects.filter(
                    user_id=uid, work_status="ongoing")
                print delay_worklist
                delayWork = worksRelationDTO.objects.filter(
                    user_id=uid, work_status="delay")
                print delay_worklist
                pendingWork = worksRelationDTO.objects.filter(
                    user_id=uid, work_status="pending")
                print pending_worklist
                for work in delayWork:
                    delay_worklist.append(str(work.work_id))
                for work in pendingWork:
                    pending_worklist.append(str(work.work_id))
                for work in ongoingWork:
                    ongoing_worklist.append(str(work.work_id))
                udict["pending"] = pending_worklist
                udict["delay"] = delay_worklist
                udict["ongoing"] = ongoing_worklist
                # username="调接口得到username"
                if username == None or username == "":
                    data[mail] = udict
                else:
                    data[username] = udict
            return data

        except BaseException, e:
            print e

    def getIssueWork(self):
        '''Get all user_id from worksRelationDTO'''
        try:
            data = {}
            userid_list = worksRelationDTO.objects.values_list(
                'user_id', flat=True)
            user_list = list(set(userid_list))
            for uid in user_list:
                udict = {}
                auth_obj = Auth.objects.get(userid=uid)
                username = auth_obj.username
                mail = auth_obj.name
                delay_worklist = []
                pending_worklist = []
                delayWork = worksRelationDTO.objects.filter(
                    user_id=uid, work_status="delay")
                print delay_worklist
                pendingWork = worksRelationDTO.objects.filter(
                    user_id=uid, work_status="pending")
                print pending_worklist
                for work in delayWork:
                    delay_worklist.append(str(work.work_id))
                for work in pendingWork:
                    pending_worklist.append(str(work.work_id))
                udict["pending"] = pending_worklist
                udict["delay"] = delay_worklist
                # username="调接口得到username"
                if username == None or username == "":
                    data[mail] = udict
                else:
                    data[username] = udict
            return data

        except BaseException, e:
            print e

    # Excel

    def get_lastweek(self, ptime):
        t = time.strptime(ptime, "%Y-%m-%d")
        standday = datetime.datetime(*t[:3]);
        daydelta = datetime.timedelta(days=1)

        lastweek = []
        tmp = standday
        for i in range(7):
            tmp -= daydelta
            lastweek.append(tmp.strftime("%Y-%m-%d"))
        return lastweek

    def get_nextweek(self, ptime):
        t = time.strptime(ptime, "%Y-%m-%d")
        standday = datetime.datetime(*t[:3]);
        daydelta = datetime.timedelta(days=1)

        nextweek = []
        tmp = standday
        for i in range(6):
            tmp += daydelta
            nextweek.append(tmp.strftime("%Y-%m-%d"))
        return nextweek

    def export(self, ptime):

        lastweek = self.get_lastweek(ptime)
        nextweek = self.get_nextweek(ptime)

        book = Workbook()
        sheet1 = book.add_sheet('Sheet 1')
        sheet1.write(0, 0, u'姓名')
        sheet1.write(0, 1, u'上周工作报告')
        sheet1.write(0, 2, u'本周工作计划')

        sheet1.col(0).width = 2800
        sheet1.col(1).width = 8000
        sheet1.col(2).width = 8000

        data_dict = {}

        # lastweek
        works = list(worksDTO.objects.filter(Status="ongoing"))
        works += list(worksDTO.objects.filter(Status="pending"))
        works += list(worksDTO.objects.filter(Status="delay"))

        st_time = time.strptime(ptime, "%Y-%m-%d")
        standday = datetime.datetime(*st_time[:3]);
        daydelta = datetime.timedelta(days=7)
        tmp = standday - daydelta
        lastweek = tmp.strftime("%Y-%m-%d")

        works += list(worksDTO.objects.filter(Status="done",
                                              StartDate__gt=lastweek))

        lastweek_dict = {}

        for work in works:
            work_info = work.summary + "(" + work.Status + ")\n"
            worksRelation = worksRelationDTO.objects.filter(work_id=work.id)

            uid = ""
            for worksRelation in worksRelation:
                uid = worksRelation.user_id

            auth_obj = Auth.objects.get(userid=uid)
            username = auth_obj.username
            mail = auth_obj.name

            if username == None or username == "":
                key = mail
            else:
                key = username

            if not data_dict.has_key(key):
                data_dict[key] = {u"last": "", u"next": ""}

            data_dict[key][u"last"] += work_info

        # lastweek
        works = list(worksDTO.objects.filter(Status="ongoing"))
        works += list(worksDTO.objects.filter(Status="delay"))

        # st_time = time.strptime(ptime, "%Y-%m-%d")
        # standday = datetime.datetime(*st_time[:3]);
        daydelta = datetime.timedelta(days=6)
        tmp = standday + daydelta
        nextweek = tmp.strftime("%Y-%m-%d")

        works += list(worksDTO.objects.filter(Status="todo",
                                              StartDate__lt=nextweek))

        nextweek_dict = {}

        for work in works:
            work_info = work.summary + "(" + work.Status + ")\n"
            worksRelation = worksRelationDTO.objects.filter(work_id=work.id)

            uid = ""
            for worksRelation in worksRelation:
                uid = worksRelation.user_id

            auth_obj = Auth.objects.get(userid=uid)
            username = auth_obj.username
            mail = auth_obj.name

            if username == None or username == "":
                key = mail
            else:
                key = username

            if not data_dict.has_key(key):
                data_dict[key] = {u"last": "", u"next": ""}

            data_dict[key][u"next"] += work_info

        i = 1
        print data_dict
        for key_name in data_dict:
            if data_dict[key_name].has_key("last"):
                print key_name
                print "last"
                print data_dict[key_name]["last"]
            if data_dict[key_name].has_key("next"):
                print key_name
                print "next"
                print data_dict[key_name]["next"]

            row = sheet1.row(i)
            row.write(0, key_name)
            row.write(1, data_dict[key_name]["last"])
            row.write(2, data_dict[key_name]["next"])
            sheet1.row(i).height_mismatch = True
            sheet1.row(i).height = 80 * 20
            i += 1

        filename = './WorkDone/static/report/WeeklyReport' + \
            time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.xls'
        print filename.encode("gbk")
        book.save(filename)
        book.save(TemporaryFile())

        return filename

    def export_self(self, uid, ptime):
        try:

            import sqlite3
            # lastweek = self.get_lastweek(ptime)
            # nextweek = self.get_nextweek(ptime)

            st_time = time.strptime(ptime, "%Y-%m-%d")
            standday = datetime.datetime(*st_time[:3]);
            daydelta = datetime.timedelta(days=7)
            tmp = standday - daydelta
            lastweek = tmp.strftime("%Y-%m-%d")

            sql3 = sqlite3.connect("db.sqlite3")

            cursor = sql3.cursor()
            sql_str = 'select WorkDone_worksdto.summary,WorkDone_worksdto.Status FROM WorkDone_worksrelationdto LEFT JOIN WorkDone_worksdto WHERE WorkDone_worksrelationdto.work_id = WorkDone_worksdto.id AND WorkDone_worksrelationdto.user_id=' + \
                str(uid) + ' AND (WorkDone_worksdto.Status="delay" OR WorkDone_worksdto.Status="ongoing" OR WorkDone_worksdto.Status="pending" OR (WorkDone_worksdto.Status="done" AND WorkDone_worksdto.DoneDate >= "' + lastweek + '"));'
            print sql_str
            cursor.execute(sql_str)
            works = cursor.fetchall()

            print works

            data_dict = {"last_week":works}
            
            st_time = time.strptime(ptime, "%Y-%m-%d")
            standday = datetime.datetime(*st_time[:3]);
            daydelta = datetime.timedelta(days=6)
            tmp = standday + daydelta
            nextweek = tmp.strftime("%Y-%m-%d")
            print nextweek
            cursor = sql3.cursor()
            sql_str = 'select WorkDone_worksdto.summary,WorkDone_worksdto.Status FROM WorkDone_worksrelationdto LEFT JOIN WorkDone_worksdto WHERE WorkDone_worksrelationdto.work_id = WorkDone_worksdto.id AND WorkDone_worksrelationdto.user_id=' + \
                str(uid) + ' AND (WorkDone_worksdto.Status="delay" OR WorkDone_worksdto.Status="ongoing" OR (WorkDone_worksdto.Status="todo" AND WorkDone_worksdto.StartDate < "' + nextweek + '"));'
            cursor.execute(sql_str)
            works = cursor.fetchall()
            
            data_dict["next_week"]=works
            print data_dict
            cursor.close()
            return 0, data_dict

        except BaseException, e:
            print e
            return 1, "error"



    @staticmethod
    def auto_update_work():
        '''Auto update Todo & Ongoing works status base on current time'''
        try:
            todoworks = worksDTO.objects.filter(Status="todo")
            today = time.strftime("%Y-%m-%d", time.localtime())
            for obwork in todoworks:
                if obwork.StartDate <= today:
                    obwork.Status = "ongoing"
                    wid = obwork.id
                    obwork.save()
                    # del obwork
                    self.update_releationWork(wid, "ongoing")
            ongoingworks = worksDTO.objects.filter(Status="ongoing")
            for obwork in ongoingworks:
                if obwork.EstimateDate <= today:
                    obwork.Status = "delay"
                    wid = obwork.id
                    obwork.save()
                    self.update_releationWork(wid, "delay")
            return 0
        except BaseException, e:
            print type(e)
            return 1, "error"

    @staticmethod
    def fix_status():
        WR_list = worksRelationDTO.objects.all()
        for cc in WR_list:
            work = worksDTO.objects.filter(id=cc.work_id)
            # print work[0].id
            cc.work_status = work[0].Status
            cc.save()
        pass
            
