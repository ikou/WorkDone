# -*- coding: utf-8 -*-
"""dao of the token"""

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class TokenDao(object):
    """class of dao of the token"""
    def __init__(self):
        #self.auth = Auth()
        pass

    def create_token(self, user):
        """create new token"""
        if user:
            print Token.objects.create(user=user)
            return 1, "created a new user"
        else:
            return 0, "the user exist"

    def get_token(self, userid):
        try:
            rest = Token.objects.get(user_id=userid)
            return 1, rest.key
        except BaseException, e:
            print type(e)
            return 0, "Exception"

    def check_token(self,token):
        try:
            rest = Token.objects.get(key=token)
            user = User.objects.get(id=rest.user_id)
            return 1, {"user_id":rest.user_id,"username":user.username}
        except BaseException, e:
            print type(e)
            return 0, "Exception"