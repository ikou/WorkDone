# -*- coding: utf-8 -*-
"""model of Authentication"""
from django.db import models


class Auth(models.Model):
    """class of user Authentication"""
    userid = models.IntegerField()
    name = models.CharField(max_length=30)
    right = models.IntegerField()
    username = models.CharField(max_length=16, null=True)
