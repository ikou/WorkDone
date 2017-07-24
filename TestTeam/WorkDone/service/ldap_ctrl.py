# -*- coding: utf-8 -*-
"""management of LDAP"""
import threading
import ldap

DL_LDAP_URL = "ldap://ldap.idanlu.com/"
BASE_DN = "dc=danlu,dc=com"

FOUNDRESULT_SERVERBUSY = "Server is busy"
FOUNDRESULT_NOTFOUND = "Not Found"
FOUNDRESULT_FOUND = "Found"
FOUNDRESULT_LOGINSUCC = "Login Success"
FOUNDRESULT_PWWRONG = "Password Wrong"

class LDAPService(object):
    """class of LDAP management"""
    _instance = None
    mutex = threading.Lock()

    @staticmethod
    def get_instance():
        '''单例模式获得实例'''
        if LDAPService._instance == None:
            LDAPService.mutex.acquire()
            if LDAPService._instance == None:
                #print u'初始化实例'
                LDAPService._instance = LDAPService()
            else:
                #print u'单例已经实例化'
                pass
            LDAPService.mutex.release()
        else:
            #print u'单例已经实例化'
            pass
        return LDAPService._instance

    def __init__(self):
        print 'create WorkDoneLogin class'
        #pass

    def validate_ldap_usermail(self, usermail):
        """verify the usermail from LDAP server"""
        try:
            print usermail
            print "step1"
            conn = None
            conn = ldap.initialize(DL_LDAP_URL)
            print "step2"
            search_scope = ldap.SCOPE_SUBTREE
            print "step3"
            #anonymous_login
            
            search_filter = '(mail=' + usermail +')'
            ldap_result_id = conn.search(BASE_DN, search_scope, search_filter)
            result_data = conn.result(ldap_result_id, 1)
            if not len(result_data[1]) == 0:
            #print result_data[1]
            #if not result_data[1]:
                return 1, result_data
            else:
                return 0, FOUNDRESULT_NOTFOUND
        except BaseException, e:
            print type(e)
            print e
            return 0, FOUNDRESULT_SERVERBUSY
        finally:
            if conn:
                del conn

    def ldap_check(self, usermail, password):
        """verify the usermail and password from LDAP server"""
        try:
            conn = None
            rest = self.validate_ldap_usermail(usermail)
            #print rest
            if rest[0] == 1:
                user_dn = rest[1][1][0][0]
                conn = ldap.initialize(DL_LDAP_URL)
                conn.set_option(ldap.OPT_REFERRALS, 0)
                conn.protocol_version = ldap.VERSION3
                conn.simple_bind_s(user_dn, password)
                return 1, FOUNDRESULT_LOGINSUCC
            else:
                return 0, rest[1]
        except BaseException, e:
            print type(e)
            return 0, FOUNDRESULT_PWWRONG
        finally:
            if conn:
                del conn
