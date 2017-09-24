# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin, \
    AbstractBaseUser, BaseUserManager
# Create your models here.


class MyManager(BaseUserManager):
    def create_user(self, name, password, **kwargs):
        now = timezone.now()
        user = self.model(name=name, is_active=True,
                        last_login=now, **kwargs)
        print 'create_user password: {0}, {1}'.format(type(password), password)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, password, **kwargs):
        now = timezone.now()
        user = self.model(name=name, is_staff=True, is_active=True,
                          is_superuser=True, last_login=now, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    TYPE_CHOICE = ((0, u'技术'), (1, u'测试'), (2, u'经理'))

    # id = models.IntegerField('ID', primary_key=True, auto_created=True)
    name = models.CharField(u'姓名', max_length=30, unique=True)
    password = models.CharField(u'密码', max_length=128)
    type = models.IntegerField(u'职位', choices=TYPE_CHOICE, default=0)
    enterTime = models.DateTimeField(u'入职时间', auto_now_add=True, editable=False)
    qq = models.CharField('QQ', max_length=12, default='')
    avatar = models.ImageField(u'头像', null=True)

    USERNAME_FIELD = 'name'
    is_active = models.BooleanField('active', default=True,
                                    help_text='Designates whether this user should be treated as '
                                              'active. Unselect this instead of deleting accounts.')
    is_staff = models.BooleanField('staff', default=False)

    objects = MyManager()

    # def passwd_hash(self, passwd):
    #     self.password = hashlib.md5(passwd).hexdigest()
    #
    # def check_passwd(self, passwd):
    #     return True if hashlib.md5(passwd).hexdigest() \
    #                    == self.password else False

    def __unicode__(self):
        return 'user {0}, name : {1}'.format(self.id, self.name)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name


