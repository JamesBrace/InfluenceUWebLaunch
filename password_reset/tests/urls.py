from django.conf.urls import url

from . import views
from ..urls import urlpatterns

urlpatterns += [
    url(r'^email_recover/$', views.email_recover, name='email_recover'),
    url(r'^username_recover/$', views.username_recover,
        name='username_recover'),
    url(r'^insensitive_recover/$', views.insensitive_recover,
        name='insensitive_recover'),
]
