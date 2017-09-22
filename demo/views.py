# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from models import User
from ser_model import UserSer

# Create your views here.


def index(req):
    return HttpResponse("welcome")


@csrf_exempt
def register(req):
    args = json.loads(req.body)
    print args
    if args:
        print 'register args: ', args
        passwd = args.pop('password')
        print passwd
        user = User.objects.create(name=args.get('username'))
        user.passwd_hash(passwd)
        user.save()
        return HttpResponse(json.dumps({'code': 1, 'data': 'success'}),
                            content_type='application/json')
    return HttpResponse(json.dumps({'code': -1, 'data': 'args error!'}),
                        content_type='application/json')


@csrf_exempt
def login(req):
    args = json.loads(req.body)
    name = args.get('username', '')
    passwd = args.get('password', '')
    print name, passwd
    user = User.objects.filter(name=name)[0]
    if user:
        print '--pass check : ', user.check_passwd(passwd)
        return HttpResponse(json.dumps({'code':1, 'data': UserSer(user).data}),
                            content_type='application/json')
    return HttpResponse(json.dumps({'code': -1, 'data': u'用户名或密码错误'}),
                        content_type='application/json')

