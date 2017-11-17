from django.db import models


# Create your models here.
class DetailData(models.Model):
    number = models.CharField(max_length=50, unique=True)
    plan_start_time = models.TimeField(null=True, blank=True)
    actual_start_time = models.TimeField(null=True, blank=True)
    plan_end_time = models.TimeField(null=True, blank=True)
    actual_end_time = models.TimeField(null=True, blank=True)
    canceled = models.BooleanField(default=False)
    manual = models.BooleanField(default=False)
    repair_type = models.CharField(max_length=50, blank=True, null=True)
    actual_start_number = models.CharField(max_length=50, blank=True, null=True)
    actual_end_number = models.IntegerField(null=True, blank=True)
    person = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField()
    department = models.ForeignKey('department.Department')
