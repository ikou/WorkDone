# -*- coding: utf-8 -*-
"""dao of the Authentication"""
from WorkDone.my_models.auth_model import Auth
from django.contrib.auth.models import User

from token_dao import TokenDao


class AuthDao(object):
    """class of dao of the Authentication"""

    def __init__(self):
        self.auth = Auth()
        # pass

    def create_user(self, username):
        """create new user"""
        if not self.verify_user(username):
            # authDTO matching query does not exist.
            user = User()
            user.username = username
            user.email = username
            user.save()

            token = TokenDao()
            token.create_token(user)

            auth = Auth()
            auth.userid = user.id
            auth.name = username
            auth.right = 1  # 默认登录后可以操作
            auth.save()

            return 1, "created a new user", token
        else:
            return 0, "the user exist"

    def verify_user(self, username):
        """verify user, if exist"""
        try:
            #auth = Auth.objects.get(name=username)
            user = User.objects.get(username=username)
            return user
        except BaseException, e:
            # Auth matching query does not exist.
            print type(e)
            return None

    def get_user_right(self, username="", userid=0):
        """verify user right by username or userid"""
        if username != "":
            try:
                auth = Auth.objects.get(name=username)
                if auth.right == 0:
                    ret = "NOT RIGHT ACCESS"
                elif auth.right == 1:
                    ret = "FOUND"
                else:
                    ret = "UNKNOWN ERROR"
                return auth.right, ret
            except BaseException, e:
                print type(e)
                return 0, "Exception"

        elif userid != 0:
            try:
                auth = Auth.objects.get(userid=userid)
                if auth.right == 0:
                    ret = "NOT RIGHT ACCESS"
                elif auth.right == 1:
                    ret = "FOUND"
                else:
                    ret = "UNKNOWN ERROR"
                return auth.right, ret
            except BaseException, e:
                print type(e)
                return 0, "Exception"
        else:
            return 0, "INVALID PARAM"
