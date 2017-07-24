# -*- coding: utf-8 -*-
"""DTO of Works"""
from django.db import models


class worksDTO(models.Model):
    """class of user works"""
    summary = models.CharField(max_length=64)
    StartDate = models.CharField(max_length=32)
    EstimateDate = models.CharField(max_length=32)
    DoneDate = models.CharField(max_length=32, null=True)
    Status = models.CharField(max_length=16, null=True)
    Notes = models.CharField(max_length=500, null=True)
    Reasons = models.CharField(max_length=64, null=True)
 