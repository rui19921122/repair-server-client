import os
import time

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


# Create your views here.
@api_view(['GET'])
def get_mock_plan_data(request):
    time.sleep(1)
    with open(r'./mock_data/plan.json', 'r', encoding='utf8') as plan:
        plan_data = json.load(plan)
    return Response(plan_data)


@api_view(['GET'])
def get_mock_history_data(request):
    time.sleep(1)
    with open(r'./mock_data/global.json', 'r', encoding='utf8') as history:
        history_data = json.load(history)
    return Response(history_data)


@api_view(["GET"])
def get_mock_detail_data(request, wx_id):
    if request.user.is_authenticated():
        time.sleep(2)
        path = os.path.join('./mock_data/data', '{}.json'.format(wx_id))
        if os.path.exists(path):
            with open(path, 'r', encoding='utf8') as detail:
                detail_data = json.load(detail)
                return Response(detail_data)
        else:
            return Response(status=404)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
