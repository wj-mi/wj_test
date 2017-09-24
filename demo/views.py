# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


from models import User
from ser_model import UserSer

# Create your views here.


def _json_serialize(data):
    return JSONRenderer().render(data)


def index(req):
    return HttpResponse("welcome")


@csrf_exempt
def register(req):
    args = json.loads(req.body)
    if args:
        print 'register args: ', args
        name = args.pop('username')
        passwd = args.pop('password')
        user = User.objects.filter(name=name)
        if user:
            return HttpResponse(json.dumps({'code': -1, 'data': u'用户名已被注册'}),
                                content_type='application/json')
        user = User.objects.create_user(name, passwd)
        if user:
            return HttpResponse(json.dumps({'code': -1, 'data': u'用户名已被注册'}), content_type='application/json')
        return HttpResponse(json.dumps({'code': 1, 'data': 'success'}),
                            content_type='application/json')
    return HttpResponse(json.dumps({'code': -1, 'data': 'args error!'}),
                        content_type='application/json')


@csrf_exempt
def per_login(req):
    args = json.loads(req.body)
    name = args.get('username', '')
    passwd = args.get('password', '')
    user = authenticate(name=name, password=passwd)
    if user is not None:
        login(req, user)
        data = {'code': 1, 'data': UserSer(user).data}
        return HttpResponse(JSONRenderer().render(data))
    return HttpResponse(json.dumps({'code': -1, 'data': u'用户名或密码错误'}),
                        content_type='application/json')


class UserView(APIView):

    def get(self, req):
        user = req.user
        print 'user {0}, type: {1}'.format(user, type(user))
        if isinstance(user, AnonymousUser):
            data = {'code': -1, 'data': u'你还没有登录哟'}
        else:
            data = {'code': 1, 'data': UserSer(user).data}
        return HttpResponse(_json_serialize(data))

    @csrf_exempt
    def put(self, req):
        user = req.user
        try:
            args = json.loads(req.body)
            for k, v in args.items():
                setattr(user, k, v)
        except ValueError:
            print '-------value error'
        if req.FILES:
            print 'file: ', dict(req.FILES)
            user.avatar = req.FILES.get('avatar', '')
        user.save()
        data = {'code': 1, 'data': UserSer(user).data}
        return HttpResponse(_json_serialize(data))


def LogOut(req):
    logout(req)
    data = {'code': 1, 'data': 'Baybay'}
    return HttpResponse(_json_serialize(data))


