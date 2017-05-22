from django.conf.urls import url, include
from .views import scrapy_from_website_history, scrapy_from_login_detail

url_names = {
    'get_repair_data_with_detail': 'get_repair_data_with_detail',
    'get_repair_single_data_with_detail': 'get_repair_single_data_with_detail'

}

urlpatterns = [
    url(
        r'^get-repair-history/(?P<start_year>\d{4})-(?P<start_month>\d{2})-(?P<start_date>\d{2})/(?P<end_year>\d{4})-(?P<end_month>\d{2})-(?P<end_date>\d{2})',
        scrapy_from_website_history,
        name='get_repair_data_with_detail'
    ),
    url(
        r'^get-repair-detail/(?P<wx_id>\d{2,7})/',
        scrapy_from_login_detail,
        name='get_repair_single_data_with_detail'
    )

]
