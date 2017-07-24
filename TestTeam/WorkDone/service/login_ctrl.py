# -*- coding: utf-8 -*-
"""management of LDAP"""

import threading
from WorkDone.dao.auth_dao import AuthDao
from WorkDone.dao.token_dao import TokenDao
from WorkDone.service.ldap_ctrl import LDAPService

class LoginService(object):
    """class of LDAP management"""
    _instance = None
    mutex = threading.Lock()

    @staticmethod
    def get_instance():
        '''单例模式获得实例'''
        if not LoginService._instance:
            LoginService.mutex.acquire()
            if not LoginService._instance:
                #print u'初始化实例'
                LoginService._instance = LoginService()
            else:
                #print u'单例已经实例化'
                pass
            LoginService.mutex.release()
        else:
            #print u'单例已经实例化'
            pass
        return LoginService._instance

    def __init__(self):
        print 'LoginService class init'
        self.ldap = LDAPService.get_instance()
        self.auth = AuthDao()
        self.token = TokenDao()
        # pass

    def __del__(self):
        if self.auth:
            del self.auth
        if self.token:
            del self.token

    def check_token(self, token):
        '''check token from db'''
        if token:
            return self.token.check_token(token)
        else:
            return 1, "invalid token"

    def login(self, usermail, password):
        '''login method the out interface'''
        #step 2: verify the usermail and password in ldap
        rest = self.ldap.ldap_check(usermail, password)
        if rest[0] == 1:
            user = self.auth.verify_user(username=usermail)
            # print user.id
            if user:
                # pass
                rest_right = self.auth.get_user_right(username=usermail)
                print "step1"
                print rest_right
                if rest_right[0] == 1:
                    token = self.token.get_token(user.id)
                    # print token
                    return 1, "succ", token[1]
                else:
                    return rest_right
            else:
                self.auth.create_user(username=usermail)
                return 1, "new user"
        else:
            return rest
