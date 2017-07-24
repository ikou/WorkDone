# -*- coding: utf-8 -*-
"""DTO of Authentication"""
from django.db import models


class authDTO(models.Model):
    """class of user Authentication"""
    name = models.CharField(max_length=30)
    right = models.IntegerField(null=True)
