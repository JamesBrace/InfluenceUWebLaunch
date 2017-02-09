from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from rest_framework_nested import routers

from InfluenceUApp.views import IndexView
from verification.views import AccountViewSet, ResendView, ActivationView, LoginView, UpdateView

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)

urlpatterns = [

    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/update/$', UpdateView.as_view(), name='update'),
    url(r'^activate/complete/$', TemplateView.as_view(template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    url(r'^api/v1/resend/', ResendView.as_view(), name='resend'),
    url(r'^api/v1/activate/(?P<activation_key>[-:\w]+)/$', ActivationView.as_view(), name='registration_activate'),
    url(r'^register/complete/$',
        TemplateView.as_view(
            template_name='registration/registration_complete.html'
        ),
        name='registration_complete'),
    url(r'^register/closed/$',
        TemplateView.as_view(
            template_name='registration/registration_closed.html'
        ),
        name='registration_disallowed'),
    url(r'', include('registration.auth_urls')),
    url(r'^forgot-password/', include('password_reset.urls')),
    url('^.*$', IndexView.as_view(), name='index'),
]
