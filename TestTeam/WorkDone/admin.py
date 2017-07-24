# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from WorkDone.my_models.auth_model import *
from WorkDone.my_models.works_model import *
from WorkDone.my_models.worksRelation_model import *

admin.site.register(Auth)
admin.site.register(worksRelationDTO)
admin.site.register(worksDTO)