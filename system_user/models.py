from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserDetailInfo(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户名')
    user = models.OneToOneField(User, related_name='user_detail_info', verbose_name='内置用户')
    department = models.ForeignKey('department.Department')