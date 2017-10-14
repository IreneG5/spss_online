from django.conf.urls import url
import views

urlpatterns = [
    url(r'^blog/$', views.post_list, name='blog'),
    url(r'^blog/(?P<post_id>\d+)/$', views.post_detail, name='post-detail'),
    url(r'^blog/voteup/(?P<post_id>\d+)/$', views.post_voteup, name='voteup'),
    url(r'^blog/votedown/(?P<post_id>\d+)/$', views.post_votedown, name='votedown'),
]
