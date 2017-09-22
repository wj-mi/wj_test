# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
from django.db import models

# Create your models here.


class User(models.Model):
    TYPE_CHOICE = ((0, u'技术'), (1, u'测试'), (2, u'经理'))

    # id = models.IntegerField('ID', primary_key=True, auto_created=True)
    name = models.CharField(u'姓名', max_length=30)
    password = models.CharField(u'密码', max_length=128, default='')
    type = models.IntegerField(u'职位', choices=TYPE_CHOICE, default=0)
    enterTime = models.DateTimeField(u'入职时间', auto_now_add=True, editable=False)
    qq = models.CharField('QQ', max_length=12, default='')
    avatar = models.ImageField(u'头像', upload_to='media', null=True)

    def passwd_hash(self, passwd):
        self.password = hashlib.md5(passwd).hexdigest()

    def check_passwd(self, passwd):
        return True if hashlib.md5(passwd).hexdigest() \
                       == self.password else False

    def __unicode__(self):
        return 'user {0}, name : {1}'.format(self.id, self.name)


