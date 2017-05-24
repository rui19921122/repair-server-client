from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/mock-data/', include("mock_data.urls")),
    url(r'^api/user/', include("user.urls")),
    url(r'^api/config/', include("web_config.urls")),
    url(r'^api/', include("rest_framework_docs.urls")),
]
