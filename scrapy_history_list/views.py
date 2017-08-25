from django.shortcuts import render
import datetime
from rest_framework import generics, permissions
from scrapy_func import get_history_list


# Create your views here.

class ScrapyHistoryListView(generics.RetrieveAPIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        print(self.request.query_params)
        try:
            start_date = datetime.datetime.strptime(self.request.query_params.get('start'), '%Y%m%d').date()
            end_date = datetime.datetime.strptime(self.request.query_params.get('end'), '%Y%m%d').date()
        except:
            raise ValueError("提供的参数缺失")
        if end_date < start_date:
            raise ValueError("日期提供错误")
        print(start_date, end_date)
