# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'demo'

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.per_login, name='login'),
    url(r'^info/$', views.UserView.as_view(), name='info'),
    url(r'^logout/$', views.LogOut, name='logout'),
]