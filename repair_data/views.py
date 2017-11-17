import datetime

from django.contrib.auth.models import User, AnonymousUser
from rest_framework import serializers, generics
# Create your views here.
from rest_framework import status
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from repair_data.models import DetailData
from system_user.models import UserDetailInfo


class RepairPlanPostDataFromClientSingleContentSer(serializers.Serializer):
    number = serializers.CharField(required=True)
    plan_start_time = serializers.DateTimeField(required=False)
    plan_end_time = serializers.DateTimeField(required=False)
    canceled = serializers.BooleanField(default=False)
    manual = serializers.BooleanField(default=False)
    actual_start_time = serializers.DateTimeField(required=False)
    actual_end_time = serializers.DateTimeField(required=False)
    actual_start_number = serializers.CharField(required=False)
    actual_end_number = serializers.CharField(required=False)
    person = serializers.CharField(required=False)

    def validate(self, data):
        if data['plan_end_time'] and data['plan_start_time']:
            if data['plan_end_time'] < data['plan_start_time']:
                raise ValidationError("计划结束时间不能早于开始时间")
        if data['actual_end_time'] and data['actual_start_time']:
            if data['actual_end_time'] < data['actual_start_time']:
                raise ValidationError("实际结束时间不能早于开始时间")


class RepairPlanPostDataFromClientListSer(serializers.Serializer):
    date = serializers.DateField(required=True)
    contents = RepairPlanPostDataFromClientSingleContentSer(many=True)

    def create(self, validated_data):
        exists = DetailData.objects.filter(
            date=validated_data['date'],
            department=validated_data['department']
        )
        if exists.count() > 0:
            # 删除已有的数据
            exists.delete()
        for i in validated_data['contents']:
            i.save()
            detail = DetailData(
                department=validated_data['department'],
                date=validated_data['date'],
                number=i['number'],
                plan_start_time=i['plan_start_time'],
                actual_start_time=i['actual_start_time'],
                plan_end_time=i['plan_end_time'],
                actual_end_time=i['actual_end_time'],
                manual=i['manual'],

            )


class DetailDataListSer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='detail-url')

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
    check_dates = set()
    print(request.data)
    for i in request.data['data']:
        check_dates.add(datetime.date(i['date']))
    print(check_dates)
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
        return request.user.is_authenticated() and UserDetailInfo.objects.get(
            user=request.user).department == obj.department


# Create your views here.

@api_view(['POST'])
def check_repair_date_conflict(request):
    """
    此处操作在向服务器发出天窗修实绩存储前发出，参数为{data: 'YYYYMMDD'[]},
    目的是为了检测将要提交的数据是否与天窗修中既有的数据冲突
    :param request:
    :return:
    """

    try:
        data = request.data['data']['date']
    except KeyError:
        return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
    return_data = []
    for i in data:
        if len(i) != 8:
            return Response(data={'error': '{}不符合规范'.format(i)}, status=status.HTTP_402_PAYMENT_REQUIRED)
        date = datetime.date(year=int(i[0:4]), month=int(i[4:6]), day=int(i[6:8]))
        return_data.append(
            {'date': date, 'conflict': True if DetailData.objects.filter(
                date=date, department=UserDetailInfo.objects.get(user=request.user).department
            ).exists() else
            False})
    return Response(data={
        'date_post': return_data
    })
