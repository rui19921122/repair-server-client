from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^post-repair-data/', views.post_detailed_data),
    url(r'^get-repair-data/', views.get_detail_data),
    url(r'check-repair-conflict-date', views.check_repair_date_conflict),
]
