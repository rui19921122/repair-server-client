from django.db import models


# Create your models here.
class DetailData(models.Model):
    number = models.CharField(max_length=50, unique=True, verbose_name='编号')
    plan_start_time = models.DateTimeField(null=True, blank=True, verbose_name='计划开始时间')
    plan_longing = models.PositiveIntegerField(default=0, verbose_name='计划时长')
    actual_start_time = models.DateTimeField(null=True, blank=True, verbose_name='实际结束时间')
    plan_end_time = models.DateTimeField(null=True, blank=True, verbose_name='计划结束时间')
    actual_end_time = models.DateTimeField(null=True, blank=True, verbose_name='实际结束时间')
    actual_longing = models.PositiveIntegerField(default=0, verbose_name='实际时长')
    canceled = models.BooleanField(default=False, verbose_name='是否被取消')
    manual = models.BooleanField(default=False, verbose_name='是否人工输入')
    actual_start_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='实际开始编号')
    actual_end_number = models.IntegerField(null=True, blank=True, verbose_name='实际结束编号')
    person = models.CharField(max_length=50, blank=True, null=True, verbose_name='把关人')
    date = models.DateField(verbose_name='日期')
    department = models.ForeignKey('department.Department', verbose_name='部门',on_delete=models.SET_NULL,null=True)
    note = models.CharField(max_length=50, verbose_name='备注', default='')
