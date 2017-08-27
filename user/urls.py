from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^login/', views.Login, name='login'),
    url(r'^user/', views.UserInfo, name='user'),
]
