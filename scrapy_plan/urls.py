from django.conf.urls import url
from . import views

urlpatterns = [
    url('plan/$', views.ScrapyPlanView.as_view(), name='查询天窗修计划历史')
]
