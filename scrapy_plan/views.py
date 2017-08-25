from django.shortcuts import render
from .serization import ScrapyPlanDetailSer
from scrapy_func.get_plan_list import get_plan_data_by_date
from rest_framework import status
import datetime
from rest_framework.generics import GenericAPIView
from config import is_in_rail_net
from rest_framework.permissions import IsAuthenticated
import time
from .models import OnDutyPersonList, ScrapyPlanCacheDetail, ScrapyPlanCacheList, ScrapyPlanContentDetail, \
    WorkWithDepartmentList

# Create your views here.
from rest_framework.response import Response


class ScrapyPlanView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
            if is_in_rail_net:
                data = get_plan_data_by_date(start_date, end_date)
            else:
                # todo 完成模拟数据的生成工作
                data = {}
            ser = ScrapyPlanDetailSer(data=data, many=True)
            if ser.is_valid():
                return Response(data={
                    'length': len(ser.data),
                    'data': ser.data
                }, )
            else:
                data_with_errors = []
                for index in range(len(ser.data)):
                    _data = ser.data[index]
                    _data['errors'] = ser.errors[index]
                    data_with_errors.append(
                        _data
                    )
                return Response(
                    data={
                        'length': len(ser.data),
                        'data': data_with_errors
                    }
                )
        else:
            pass
