# -*- coding: utf-8 -*-
"""management of works"""
import threading
from WorkDone.dao.work_dao import WorksDAO


class WorksServices(object):
    """class of LDAP management"""
    _instance = None
    mutex = threading.Lock()

    @staticmethod
    def get_instance():
        '''单例模式获得实例'''
        if not WorksServices._instance:
            WorksServices.mutex.acquire()
            if not WorksServices._instance:
                # print u'初始化实例'
                WorksServices._instance = WorksServices()
            else:
                # print u'单例已经实例化'
                pass
            WorksServices.mutex.release()
        else:
            # print u'单例已经实例化'
            pass
        return WorksServices._instance

    def __init__(self):
        self.works = WorksDAO()

    def __del__(self):
        if self.works:
            del self.works

    def new_work(self, uid, summary, start_date, estimate_date):
        '''Create a work data'''
        return self.works.new_work(uid, summary, start_date, estimate_date)

    def update_work(self, work_id, status=None, notes=None, reasons=None):
        '''Update a work data'''
        return self.works.update_work(work_id, status, notes, reasons)

    def get_worklist(self, uid, status=None):
        '''Get personal work list'''
        return self.works.getWorkList(uid, status)

    def get_workinfo(self, work_id):
        '''Get one work detailed info'''
        return self.works.getWorkInfo(work_id)

    def get_issuework(self):
        '''Get all user_id from worksRelationDTO'''
        return self.works.getIssueWork()

    def get_issuework_v2(self):
        '''Get all user_id from worksRelationDTO'''
        return self.works.getIssueWork_v2()

    def export(self, day):
        '''export the weekly report'''
        return self.works.export(day)

    def export_self(self, uid, day):
        '''export the weekly report'''
        return self.works.export_self(uid, day)
