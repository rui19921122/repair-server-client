from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^post-repair-data/', views.post_detailed_data),
    url(
        r'^get-data/(?P<start_year>\d{4})-(?P<start_month>\d{2})-(?P<start_date>\d{2})/(?P<end_year>\d{4})-(?P<end_month>\d{2})-(?P<end_date>\d{2})',
        views.get_detailed_data_list,
        name='get_repair_data_with_detail'
    ),
    url(r'detail/(?P<pk>\d{1,5})', views.get_detailed_data.as_view(), name='detail-url'),
    url(r'check-repair-conflict-date', views.check_repair_date_conflict)
]
