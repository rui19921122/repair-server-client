from django.db import models
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from scrapy_func.get_repair_detail import get_repair_detail_by_inner_id
from .models import PlanHistoryDetailCache


@api_view(["GET"])
def get_history_detail(request, pk):
    try:
        s = PlanHistoryDetailCache.objects.get(inner_id=pk)
        data = {
            "number": s.number,  # 施工维修编号，格式为[JDZ]\d{3}
            "repair_content": s.repair_content,  # 施工项目
            "effect_area": s.effect_area,  # 影响使用范围
            "publish_start_time": s.publish_start_time,  # 命令号发布时间
            "publish_start_number": s.publish_start_number,  # 开始施工命令号码
            "actual_start_time": s.actual_start_time,  # 施工开始时间
            "actual_end_time": s.actual_end_time,  # 命令号结束时间
            "actual_end_number": s.actual_end_number,  # 开通施工命令号码
            "actual_host_person": s.actual_host_person,  # 把关人
        }
        return Response(data=data)
    except models.ObjectDoesNotExist:
        return Response(data=get_repair_detail_by_inner_id(pk))
