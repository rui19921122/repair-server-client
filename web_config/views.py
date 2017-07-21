from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import RepairCollectionsTableConfig
import json


# Create your views here.

class CollectionConfig(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        config = RepairCollectionsTableConfig.objects.filter(
            user_id=request.user
        ).order_by('id')
        if config.count() > 0:
            return Response(data=
            {
                'data': json.loads(config[config.count() - 1].config, encoding='utf-8')
            })
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        config = RepairCollectionsTableConfig(
            config=json.dumps(request.data, ensure_ascii=False),
            user=request.user
        )
        config.save()
        return Response(status=status.HTTP_201_CREATED)
