import datetime
import time

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework.response import Response

from scrapy_func.get_plan_list import get_plan_data_by_date
from .models import ScrapyPlanCacheList
from .serization import ScrapyPlanDetailSer


class ScrapyPlanView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print('开始爬取')
        try:
            start_date_string = self.request.query_params.get('start_date')
            end_date_string = self.request.query_params.get('end_date')
            start_date = datetime.date(*time.strptime(start_date_string, '%Y-%m-%d')[:3])
            end_date = datetime.date(*time.strptime(end_date_string, '%Y-%m-%d')[:3])
            force_update = self.request.query_params.get('force_update') or False
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': '请求的参数缺失或不合法'}
            )
        if force_update or not ScrapyPlanCacheList.objects.filter(start_date=start_date, end_date=end_date).exists():
            # 从网页上请求
            data = get_plan_data_by_date(start_date, end_date)
            ser = ScrapyPlanDetailSer(data, many=True)
            return Response(data={
                'length': len(data),
                'data': data
            }, )
        else:
            pass
