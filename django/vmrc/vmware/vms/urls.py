#vms/url.py
from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<server_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<server_id>[0-9]+)/refresh/$', views.refresh, name='refresh'),
    # ex: /polls/5/vote/
    url(r'^(?P<server_id>[0-9]+)/vote/$', views.vote, name='vote'),
    ]