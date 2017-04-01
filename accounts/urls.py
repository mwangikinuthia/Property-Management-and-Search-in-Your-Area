from django.conf.urls import url
from . import views
# maps url patterns to viewa
urlpatterns=[
# url(r'^login/$',views.user_log, name='login'),
url(r'^register/$',views.register,name='register'),
url(r'^login/$', views.user_log, name='login'),
url(r'^logout/$','django.contrib.auth.views.logout', name='logout'),
url(r'^logout-then-login/$','django.contrib.auth.views.logout_then_login',name='log_out_then_login'),
url(r'^$', views.myboard, name='myboard'),
url(r'^password-change/$', 'django.contrib.auth.views.password_change', name='password_change'),
url(r'^password-change/done/$','django.contrib.auth.views.password_change_done',name='password_change_done'),
url(r'^password-reset/$',
'django.contrib.auth.views.password_reset',
name='password_reset'),
url(r'^password-reset/done/$','django.contrib.auth.views.password_reset_done',name='password_reset_done'),
url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
'django.contrib.auth.views.password_reset_confirm',
name='password_reset_confirm'),
url(r'^password-reset/complete/$',
'django.contrib.auth.views.password_reset_complete',
name='password_reset_complete'),
url(r'^caretaker-register/$',views.registerCaretaker, name="register_caretaker"),
url(r'^caretaker-login/$',views.caretaker_log, name="log_caretaker"),
url(r'^edit/$', views.edit, name='edit'),
url(r'^profile/(?P<user_id>\d+)$', views.profile_view, name='profile'),
url(r'^profile-b/(?P<username>\w+)$', views.profile_view_2, name='profile2')
]
