"""TestTeam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from WorkDone import views as WorkDone_views  # new

from django.conf.urls import url, include
from rest_framework import routers
#from tutorial.quickstart import views


urlpatterns = [
    url(r'^$', WorkDone_views.index),  # new
    url(r'^myDashBoard$', WorkDone_views.my_dashboard),  # new
    url(r'^IssueView$', WorkDone_views.leader_dashboard),  # new
    url(r'^WeeklyReport$', WorkDone_views.weekly_report),  # new
    url(r'^admin_sync/$', WorkDone_views.admin_sync),  # new
    url(r'^hello/$', WorkDone_views.hello),  # new
    url(r'^workdone/login/$', WorkDone_views.login),  # new
    url(r'^workdone/getWorkList/$', WorkDone_views.get_worklist),  # new
    url(r'^workdone/getWorkById/$', WorkDone_views.get_work_by_id),  # new
    url(r'^workdone/CreateWork/$', WorkDone_views.create_work),  # new
    url(r'^workdone/UpdateWork/$', WorkDone_views.update_work),  # new
    url(r'^workdone/QueryIssueList_V1/$', WorkDone_views.query_issuelist),  # new
    url(r'^workdone/QueryIssueList_V2/$', WorkDone_views.query_issuelist_v2),  # new
    url(r'^workdone/getWeeklyReport/$', WorkDone_views.get_weeklyreport),  # new
    url(r'^workdone/getselfWeeklyReport/$', WorkDone_views.get_self_weeklyreport),  # new

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
]
