from django.db import models


# Create your models here.
class OnDutyPersonList(models.Model):
    """
    负责人外键
    """
    name = models.CharField(max_length=20, verbose_name='姓名')


class WorkWithDepartmentList(models.Model):
    """
    配合单位外键
    """
    name = models.CharField(max_length=20, verbose_name='部门')


class ScrapyPlanCacheList(models.Model):
    date = models.DateField(verbose_name='日期')
    details = models.ManyToManyField('scrapy_plan.ScrapyPlanContentDetail', verbose_name='内容')
    update_time = models.DateTimeField(verbose_name='更新日期', auto_now=True)


class ScrapyPlanCacheDetail(models.Model):
    number = models.CharField(max_length=4, verbose_name='编号')
    post_date = models.DateField(verbose_name='日期')
    type = models.CharField(max_length=10, verbose_name='类型')
    direction = models.CharField(max_length=10, verbose_name='行别')
    area = models.CharField(max_length=50, verbose_name='维修区域')
    plan_time = models.CharField(max_length=50, verbose_name='维修时间')
    apply_place = models.CharField(max_length=50, verbose_name='工作内容')


class ScrapyPlanContentDetail(models.Model):
    work_department = models.CharField(max_length=20, verbose_name='作业单位')
    work_place = models.CharField(max_length=20, verbose_name='作业地点')
    work_project = models.CharField(max_length=50, verbose_name='作业项目')
    work_detail = models.CharField(max_length=50, verbose_name='作业明细')
    off_power_unit = models.CharField(max_length=50, verbose_name='停电单元')
    work_vehicle = models.BooleanField(verbose_name='作业车配合')
    protect_mileage = models.CharField(verbose_name='防护里程', max_length=50)
    on_duty_person = models.ManyToManyField(OnDutyPersonList, verbose_name='负责人')
    operate_track_switch = models.BooleanField(verbose_name='是否搬动道岔', )
    work_with_department = models.ManyToManyField(WorkWithDepartmentList, verbose_name='配合单位', )
    extra_message = models.CharField(verbose_name='补充作业事项', max_length=50)
