from django.db import models


# Create your models here.

class MockPlanHistoryList(models.Model):
    """
    模拟数据从2010年1月1日开始计算天数，然后与三整除的余数即为date_start的值
    """
    date_start = models.PositiveSmallIntegerField(choices=((0, '第一天'), (1, '第二天'), (2, '第三天')))
    plan_type = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    plan_time = models.CharField(max_length=100)
    repair_content = models.CharField(max_length=100)
    repair_department = models.CharField(max_length=100)
    apply_place = models.CharField(max_length=100)
    inner_id = models.CharField(max_length=100)
    use_paper = models.BooleanField(default=False)


class MockPlanHistoryDetail(models.Model):
    """
    模拟数据以inner_id为主
    """
    number = models.CharField(max_length=100)  # 施工维修编号，格式为[JDZ]\d{3}
    repair_content = models.CharField(max_length=100)  # 施工项目
    effect_area = models.CharField(max_length=100)  # 影响使用范围
    publish_start_time = models.CharField(max_length=100)  # 命令号发布时间
    publish_start_number = models.CharField(max_length=100)  # 开始施工命令号码
    actual_start_time = models.CharField(max_length=100)  # 施工开始时间
    actual_end_time = models.CharField(max_length=100)  # 命令号结束时间
    actual_end_number = models.CharField(max_length=100)  # 开通施工命令号码
    actual_host_person = models.CharField(max_length=100)  # 把关人
    inner_id = models.CharField(max_length=100)


class MockRepairPlan(models.Model):
    pass
