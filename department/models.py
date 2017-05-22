from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    username = models.CharField(max_length=20, verbose_name='系统内名称')
    password = models.CharField(max_length=20, verbose_name='系统内密码')


class InnerUser(models.Model):
    username = models.CharField(max_length=20)
    user = models.OneToOneField(User, related_name='inner_user')
    department = models.ForeignKey('department.Department')
