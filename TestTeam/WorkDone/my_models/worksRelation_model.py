# -*- coding: utf-8 -*-
"""DTO of WorksRelation"""
from django.db import models


class worksRelationDTO(models.Model):
    """class of user works"""
    user_id = models.IntegerField()
    work_id = models.IntegerField()
    work_status = models.CharField(max_length=32)
 