from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'detail/(?P<pk>\d{1,7})', views.get_history_detail, name='history-detail-url')
]