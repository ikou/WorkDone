#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

#from rest_framework.authtoken.models import Token

for user in User.objects.all():
    print user
