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
    passwd = models.CharField('encoded passwod', max_length=100)
    hint   = models.CharField(max_length=255, blank=True)
    status = models.IntegerField()
    add_time = models.DateTimeField(default=now)
    chg_time = models.DateTimeField(default=now)

    @classmethod
    def make_passwd(cls, passwd):
        return encrypt(passwd)

    @classmethod
    def new(cls, **kwargs):
        pwd = kwargs.get('passwd', None)
        if not pwd:
            raise ValueError('passwd required')
        pwd = cls.make_passwd(pwd)
        kwargs['passwd'] = pwd
        return cls(**kwargs)

