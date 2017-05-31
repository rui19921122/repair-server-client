import datetime

from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status

from department.models import Department, InnerUser

from .models import DetailData


class DetailDataSer(serializers.ModelSerializer):
    class Meta:
        exclude = ['date', 'department']
        include = ['plan_start_time']
        model = DetailData

    def validate__plan_start_time(self, value):
        return True

    def validate__plan_end_time(self, value):
        return True

    def validate__actual_start_time(self, value):
        return True

    def validate__actual_end_time(self, value):
        return True


@api_view(["POST"])
def post_detailed_data(request):
    assert isinstance(request.user, User) or isinstance(request.user, AnonymousUser)
    if request.user.is_authenticated():
        department = InnerUser.objects.get(user=request.user).department
    else:
        return Response(status=403)
    data = DetailDataSer(data=request.data, many=True)
    if data.is_valid():
        data.save()
        return Response(status=200)
    else:
        print(data.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=data.errors
                        )
