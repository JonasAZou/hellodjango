from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class Password(models.Model):
    passwd = models.CharField('encoded passwod', max_length=100)
    hint   = models.CharField(max_length=255)

