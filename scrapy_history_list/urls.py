from django.conf.urls import url, include
from . import views

scrapy_history_list_urls = {
    'get_repair_history_list': 'get_repair_history_list',
    'get_build_history_list': 'get_build_history_list',
}

urlpatterns = [
    url(
        'repair', views.ScrapyHistoryListView.as_view(), name=scrapy_history_list_urls['get_repair_history_list']
    )
]
