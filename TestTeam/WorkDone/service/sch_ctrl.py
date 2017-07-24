# -*- coding: utf-8 -*-
"""management of LDAP"""

import threading
from datetime import datetime
import time
import os
from WorkDone.dao.work_dao import WorksDAO

from apscheduler.schedulers.background import BackgroundScheduler


def test():
    print "test"


class SchService(object):
    """class of LDAP management"""
    _instance = None
    mutex = threading.Lock()

    @staticmethod
    def get_instance():
        '''单例模式获得实例'''
        if not SchService._instance:
            SchService.mutex.acquire()
            if not SchService._instance:
                # print u'初始化实例'
                SchService._instance = SchService()
            else:
                # print u'单例已经实例化'
                pass
            SchService.mutex.release()
        else:
            # print u'单例已经实例化'
            pass
        return SchService._instance

    def __init__(self):
        print 'SchService class init'
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(WorksDAO.auto_update_work, 'cron', hour='01')
        # pass

    def __del__(self):
        pass

    def start_sch(self):
        '''start sch'''
        self.scheduler.start()
        pass

    def stop_sch(self):
        '''stop sch'''
        self.scheduler.shutdown()
        pass
