# -*- coding:utf-8 -*-

from rest_framework import serializers


from datetime import datetime


class User(object):
    def __init__(self, id, name, type, enterTime, qq):
        self.id = id
        self.name = name
        self.type = type
        self.enterTime = enterTime or datetime.now()
        self.qq = qq

# user = User(email='leila@example.com', content='foo bar')


class UserSer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=30)
    type = serializers.IntegerField()
    enterTime = serializers.DateTimeField()
    qq = serializers.CharField(max_length=20)
    avatar = serializers.ImageField()

