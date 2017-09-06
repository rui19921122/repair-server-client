from .models import ScrapyPlanCacheDetail
from rest_framework import serializers


class ScrapyPlanDetailSer(serializers.Serializer):
    number = serializers.CharField(max_length=4, verbose_name='编号')

    def validate_number(self, value):
        """
        编号，格式为4位数字
        :param value: str
        :return:
        """
        pass

    post_date = serializers.DateField(verbose_name='日期')
    type = serializers.CharField(max_length=10, verbose_name='类型')
    direction = serializers.CharField(max_length=10, verbose_name='行别')
    area = serializers.CharField(max_length=50, verbose_name='维修区域')
    plan_time = serializers.CharField(max_length=50, verbose_name='维修时间')
    apply_place = serializers.CharField(max_length=50, verbose_name='工作内容')
    content = ScrapyPlanDetailContentSer(many=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        depth = 2


class ScrapyPlanDetailContentSer(serializers.Serializer):
    work_department = serializers.CharField(max_length=20, verbose_name='作业单位')
    work_place = serializers.CharField(max_length=20, verbose_name='作业地点')
    work_project = serializers.CharField(max_length=50, verbose_name='作业项目')
    work_detail = serializers.CharField(max_length=50, verbose_name='作业明细')
    off_power_unit = serializers.CharField(max_length=50, verbose_name='停电单元')
    work_vehicle = serializers.BooleanField(verbose_name='作业车配合')
    protect_mileage = serializers.CharField(verbose_name='防护里程', max_length=50)
    on_duty_person = OnDutyPersonSer(many=True)
    operate_track_switch = serializers.BooleanField(verbose_name='是否搬动道岔', )
    work_with_department = WorkWithDepartmentSer(many=True)
    extra_message = serializers.CharField(verbose_name='补充作业事项', max_length=50)


class OnDutyPersonSer(serializers.Serializer):
    """
    负责人
    """
    name = serializers.CharField()


class WorkWithDepartmentSer(serializers.Serializer):
    """
    配合单位
    """
    name = serializers.CharField()
