from django.conf.urls import url, include
from .views import *

url_names = {
    'get_repair_data_with_detail': 'get_repair_data_with_detail',
    'get_repair_single_data_with_detail': 'get_repair_single_data_with_detail'

}

urlpatterns = [
    url(
        r'^get-repair-plan/(?P<start_year>\d{4})-(?P<start_month>\d{2})-(?P<start_date>\d{2})/(?P<end_year>\d{4})-(?P<end_month>\d{2})-(?P<end_date>\d{2})',
        open_plan_scrapy_view,
        name='get_open_plan'
    ),

]
