from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    url(r'^login/', csrf_exempt(views.login_view), name='用户登录'),
    url(r'^system-user/', csrf_exempt(views.user_info_view), name='用户信息'),
    url(r'^username-autocomplete/', views.username_autocomplete, name='自动补全'),
]
