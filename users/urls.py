from django.conf.urls import patterns, url
import views
urlpatterns = patterns(
    '',
    url(r'^login/$', 'o2w.users.views.login', name='user-login'),
    url(r'^logout/$', 'o2w.users.views.logout', name='user-logout'),
    url(r'^signup/$', views.SignupView.as_view(), name='user-signup'),
)
