import time
from django.contrib.auth import login
from django.contrib.auth.models import User, AnonymousUser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from department.models import Department
from .models import UserDetailInfo


@api_view(['GET'])
def user_info_view(request):
    """
    :param request: 
    :return: 
    """
    assert isinstance(request.user, User) or isinstance(request.user, AnonymousUser)
    if request.user.is_authenticated():
        user = UserDetailInfo.objects.get(
            user=request.user
        )
        return Response(
            data={
                'message': '成功',
                'username': user.username,
                'department': user.department.name,
                'department_username': user.department.username,
                'department_password': user.department.password
            },
        )
    else:
        return Response(data={'error': '未登陆'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def login_view(request):
    """
    :param request: 
    :return: 
    """
    assert isinstance(request.user, User) or isinstance(request.user, AnonymousUser)
    if request.user.is_authenticated():
        return Response(
            data={'error': '您已经登陆，请<a href="api/system_user/logout/">登出</a>后重试'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        try:
            user = UserDetailInfo.objects.filter(username=request.data.get('username'))
            if user.count() == 1:
                user = user[0]
            elif user.count() == 0:
                user = User.objects.filter(username=request.data.get('username'))
                if user.count() == 1:
                    user = UserDetailInfo.objects.get(user_id=user[0].id)
                else:
                    raise ValueError("username is not found")
        except ValueError:
            return Response(
                data={'error': '未找到该用户'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user.user.check_password(request.data['password']):
            login(request, user.user)
            return Response(
                data={
                    'message': '登陆成功',
                    'username': user.username,
                    'department': user.department.name,
                    'department_username': user.department.username,
                    'department_password': user.department.password
                }
            )
        else:
            return Response(
                data={'error': '登陆失败，密码错误'},
                status=status.HTTP_400_BAD_REQUEST,
            )
