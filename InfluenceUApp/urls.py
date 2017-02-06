from django.conf.urls import url, include

from InfluenceUApp.views import IndexView

from rest_framework_nested import routers

from verification.views import AccountViewSet, ResendView

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)

urlpatterns = [

    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/resend/', ResendView.as_view(), name='resend'),
    url('^.*$', IndexView.as_view(), name='index'),
]