import time
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


# Create your views here.
@api_view(['GET'])
def get_mock_plan_data(request):
    time.sleep(1)
    print(11234)
    with open(r'./mock_data/plan.json', 'r', encoding='utf8') as plan:
        plan_data = json.load(plan)
    return Response(plan_data)


@api_view(['GET'])
def get_mock_history_data(request):
    time.sleep(1)
    print(11234)
    with open(r'./mock_data/global.json', 'r', encoding='utf8') as history:
        history_data = json.load(history)
    return Response(history_data)
