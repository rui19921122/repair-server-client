from .models import ScrapyPlanCacheDetail
from rest_framework import serializers
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



class ScrapyPlanDetailContentSer(serializers.Serializer):
    work_department = serializers.CharField()
    work_place = serializers.CharField()
    work_project = serializers.CharField()
    work_detail = serializers.CharField()
    off_power_unit = serializers.CharField()
    work_vehicle = serializers.BooleanField()
    protect_mileage = serializers.CharField()
    on_duty_person = OnDutyPersonSer(many=True)
    operate_track_switch = serializers.BooleanField()
    work_with_department = WorkWithDepartmentSer(many=True)
    extra_message = serializers.CharField()




class ScrapyPlanDetailSer(serializers.Serializer):
    number = serializers.CharField()  # 编号

    def validate_number(self, value):
        """
        编号，格式为4位数字
        :param value: str
        :return:
        """
        if len(value) != 4:
            raise ValueError("编号必须为4位数")
        try:
            int(value)
        except ValueError:
            raise ValueError("编号必须为整数")

    post_date = serializers.DateField()  # 日期
    type = serializers.CharField()  # 类型
    direction = serializers.CharField()  # 行别
    area = serializers.CharField()  # 维修区域
    plan_time = serializers.CharField()  # 维修时间
    apply_place = serializers.CharField()  # 工作内容
    content = ScrapyPlanDetailContentSer(many=True)
    id = serializers.IntegerField(read_only=True)
