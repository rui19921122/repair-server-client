from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from scrapy_func.get_repair_detail import get_repair_detail_by_inner_id


@api_view(["GET"])
def get_history_detail(request, pk):
    return Response(data=get_repair_detail_by_inner_id(pk))
