#-*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .crypto import encrypt, decrypt

__all__ = ['Password']

# Create your models here.
def now():
    return timezone.now()

class Password(models.Model):
    STATUS_OK = 32
    STATUS_DELETE = 128
    STATUS_CHOICES = (
        (STATUS_OK, u'正常'),
        (STATUS_DELETE, u'删除'),
    )

    user = models.ForeignKey(User, related_name='key')
    site = models.CharField('site name', max_length=40)
    loginname = models.CharField('login name', max_length=100)
    password = models.CharField('encoded passwod', max_length=100)
    hint   = models.CharField(max_length=255, blank=True)
    status = models.IntegerField(default=STATUS_OK)
    add_time = models.DateTimeField(default=now)
    chg_time = models.DateTimeField(default=now)

    @classmethod
    def make_passwd(cls, passwd):
        return encrypt(passwd)

    @classmethod
    def new(cls, **kwargs):
        pwd = kwargs.get('password', None)
        if not pwd:
            raise ValueError('password required')
        pwd = cls.make_passwd(pwd)
        kwargs['password'] = pwd
        return cls(**kwargs)

    @classmethod
    def default_list(cls, user):
        return cls.objects.filter(user=user, status=cls.STATUS_OK).order_by('-chg_time', 'site')

