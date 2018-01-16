from django.db import models


# Create your models here.

class PlanHistoryDetailCache(models.Model):
    number = models.CharField(max_length=100)  # 施工维修编号，格式为[JDZ]\d{3}
    repair_content = models.CharField(max_length=100)  # 施工项目
    effect_area = models.CharField(max_length=100)  # 影响使用范围
    publish_start_time = models.CharField(max_length=100)  # 命令号发布时间
    publish_start_number = models.CharField(max_length=100)  # 开始施工命令号码
    actual_start_time = models.CharField(max_length=100)  # 施工开始时间
    actual_end_time = models.CharField(max_length=100)  # 命令号结束时间
    actual_end_number = models.CharField(max_length=100)  # 开通施工命令号码
    actual_host_person = models.CharField(max_length=100)  # 把关人
    inner_id = models.CharField(max_length=100, unique=True)
