import datetime

from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status, generics

from department.models import Department
from system_user.models import UserDetailInfo

from .models import DetailData


class DetailDataSer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='detail-url')

    class Meta:
        model = DetailData
        exclude = ['department']

    def create(self, validated_data):
        Detail = DetailData(
            **validated_data
        )
        Detail.date = validated_data['date']
        Detail.department = validated_data['department']
        Detail.save()
        return Detail


@api_view(["POST"])
def post_detailed_data(request):
    assert isinstance(request.user, User) or isinstance(request.user, AnonymousUser)
    if request.user.is_authenticated():
        department = UserDetailInfo.objects.get(user=request.user).department
    else:
        return Response(status=403)
    data = DetailDataSer(data=request.data, many=True)
    if data.is_valid():
        data.save(department=department)
        return Response(status=201)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=data.errors
                        )


@api_view(['GET'])
def get_detailed_data_list(request, start_year, start_month, start_date, end_year, end_month, end_date):
    start = datetime.date(int(start_year), int(start_month), int(start_date))
    end = datetime.date(int(end_year), int(end_month), int(end_date))
    assert isinstance(request.user, User) or isinstance(request.user, AnonymousUser)
    if request.user.is_authenticated():
        department = UserDetailInfo.objects.get(user=request.user).department
    else:
        return Response(status=403)
    return Response(
        data=DetailDataSer(
            DetailData.objects.filter(date__gte=start, date__lte=end, department=department),
            context={'request': request},
            many=True).data)


class get_detailed_data(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetailData.objects.all()
    serializer_class = DetailDataSer

    def check_object_permissions(self, request, obj):
        return request.user.is_authenticated() and UserDetailInfo.objects.get(user=request.user).department == obj.department
