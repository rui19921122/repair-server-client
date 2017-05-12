from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^mock-plan-data/', views.get_mock_plan_data),
    url(r'^mock-history-data/', views.get_mock_history_data),
    url(r'^mock-detail-data/(\d{1,9})', views.get_mock_detail_data),
]
