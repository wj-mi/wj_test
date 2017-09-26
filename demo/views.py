# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated



from models import User
from ser_model import UserSer

# Create your views here.


def _json_response(data):
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
            return HttpResponse(_json_response({'code': -1, 'data': u'用户名已被注册'}))
        user = User.objects.create_user(name, passwd)
        print '----user', user
        return HttpResponse(_json_response({'code': 1, 'data': 'success'}))
    return HttpResponse(_json_response({'code': -1, 'data': 'args error!'}))


# @csrf_exempt
# def per_login(req):
#     args = json.loads(req.body)
#     name = args.get('username', '')
#     passwd = args.get('password', '')
#     user = authenticate(name=name, password=passwd)
#     if user is not None:
#         login(req, user)
#         user_obj = UserSer(user).data
#         user_obj['token'] = user.set_token()
#         data = {'code': 1, 'data': user_obj}
#         return Response(data)
#     return Response({'code': -1, 'data': u'用户名或密码错误'})


class UserLogin(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print 'serializer error'
            return Response({'code': -1, 'data': u'用户名或密码错误'})
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserView(APIView):
    def get(self, req):
        user = req.user
        print 'user {0}, type: {1}'.format(user, type(user))
        if isinstance(user, AnonymousUser):
            data = {'code': -1, 'data': u'你还没有登录哟'}
        else:
            data = {'code': 1, 'data': UserSer(user).data}
        return HttpResponse(_json_response(data))
        # return HttpResponse(_json_serialize(data))

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
        return HttpResponse(_json_response(data))


def LogOut(req):
    logout(req)
    data = {'code': 1, 'data': 'Baybay'}
    return Response(data)


