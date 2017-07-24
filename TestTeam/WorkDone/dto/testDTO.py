# -*- coding: utf-8 -*-
"""DTO of Works"""
from django.db import models


class testDTO(models.Model):
    """class of user works"""
    summary = models.CharField(max_length=64)
    StartDate = models.CharField(max_length=32)
    EstimateDate = models.CharField(max_length=32)
    DoneDate = models.CharField(max_length=32)
    Status = models.CharField(max_length=16)
    Notes = models.CharField(max_length=500)
    Reasons = models.CharField(max_length=64)
