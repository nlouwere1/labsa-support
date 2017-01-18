from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', include('vms.urls')),
    url(r'^vms/', include('vms.urls')),
    url(r'^admin/', admin.site.urls),
]
