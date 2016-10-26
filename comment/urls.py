from django.conf.urls import url

from . import views

app_name = 'comment'
urlpatterns = [
    url(r'^$', views.get_comments, name='index'),
    url(r'post$', views.post_comment),
    url(r'get$', views.next_comment),
]
