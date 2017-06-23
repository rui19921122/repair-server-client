from django.db import models


# Create your models here.
class DetailData(models.Model):
    repair_check_in_method = models.CharField(max_length=50, null=True, blank=True)
    plan_id = models.CharField(max_length=50, unique=True)
    plan_work_during = models.IntegerField()
    actual_end_time = models.TimeField(null=True, blank=True)
    plan_start_time = models.TimeField(null=True, blank=True)
    actual_start_time = models.TimeField(null=True, blank=True)
    plan_end_time = models.TimeField(null=True, blank=True)
    inner_id = models.CharField(max_length=50, blank=True, null=True)
    repair_type = models.CharField(max_length=50, blank=True, null=True)
    actual_start_number = models.CharField(max_length=50, blank=True, null=True)
    actual_person = models.CharField(max_length=50, blank=True, null=True)
    repair_check_in_area = models.CharField(max_length=50, blank=True, null=True)
    repair_area = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField()
    actual_work_during = models.IntegerField()
    repair_unit = models.CharField(max_length=50, blank=True, null=True)
    actual_end_number = models.IntegerField(null=True, blank=True)
    department = models.ForeignKey('department.Department')
