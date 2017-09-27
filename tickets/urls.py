from django.conf.urls import url
import views

urlpatterns = [
    url(r'^tickets/$', views.tickets_list, name='tickets-list'),
    url(r'^tickets/(?P<ticket_id>\d+)/$', views.ticket_detail, name='ticket-detail'),
    url(r'^new_ticket/$', views.new_ticket, name='new-ticket'),
    url(r'^new_comment/(?P<ticket_id>\d+)/$', views.new_comment, name='new-comment'),
    url(r'^close_ticket/(?P<ticket_id>\d+)/$', views.close_ticket, name='close-ticket'),
    url(r'^reopen_ticket/(?P<ticket_id>\d+)/$', views.reopen_ticket, name='reopen-ticket'),
    # Edit comment not working
    url(r'^comment/edit/(?P<ticket_id>\d+)/(?P<comment_id>\d+)/$', views.edit_comment, name='edit-comment'),
    ###############
    url(r'^comment/delete/(?P<ticket_id>\d+)/(?P<comment_id>\d+)/$', views.delete_comment, name='delete-comment'),
]
