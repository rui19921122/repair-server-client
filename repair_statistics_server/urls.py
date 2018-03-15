from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/scrapy/plan/', include("scrapy_plan.urls")),
    url(r'^api/scrapy/history-list/', include("scrapy_history_list.urls")),
    url(r'^api/scrapy/history-detail/', include("scrapy_history_detail.urls")),
    url(r'^api/system-user/', include("system_user.urls")),
    url(r'^api/config/', include("web_config.urls")),
    url(r'^api/data/', include("repair_data.urls")),
]
