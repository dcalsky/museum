from django.conf.urls import url
from . import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<part_name>\w+)$', views.part, name='part'),
    url(r'^(?P<part_name>\w+)/(?P<article_id>\d+)$', views.article, name='article'),
    url(r'^appoint$', views.apply_appoint, name='appoint'),
]
