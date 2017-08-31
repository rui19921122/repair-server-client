from django.shortcuts import render
import datetime
from rest_framework import generics, permissions
from rest_framework.response import Response

from config import is_in_rail_net
from scrapy_func.get_history_list import get_repair_plan_list, generate_repair_plan_list


# Create your views here.

class ScrapyHistoryListView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        try:
            start_date = datetime.datetime.strptime(self.request.query_params.get('start'), '%Y%m%d').date()
            end_date = datetime.datetime.strptime(self.request.query_params.get('end'), '%Y%m%d').date()
        except:
            raise ValueError("提供的参数缺失")
        if end_date < start_date:
            raise ValueError("日期提供错误")
        if is_in_rail_net:
            data = get_repair_plan_list(start_date, end_date)
        else:
            data = generate_repair_plan_list(start_date, end_date)
        return Response(data={'data': data})