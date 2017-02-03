from django.conf.urls import url

from InfluenceUApp.views import IndexView

urlpatterns = [
    url('^.*$', IndexView.as_view(), name='index'),
]
