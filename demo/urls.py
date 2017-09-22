# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'demo'

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login')
]