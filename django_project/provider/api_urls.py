# coding=utf-8
"""URLs for Provider app API."""

from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from provider.api_views.provider import ProviderAPIView
from provider.api_views.service_area import ServiceAreaAPIView


urlpatterns = [
    url(r'^docs/', include_docs_urls(title='Mozio API')),
    url(r'^provider/',
        ProviderAPIView.as_view(),
        name="provider"),

    url(r'^service-area/',
        ServiceAreaAPIView.as_view(),
        name="service-area"),

    url(r'^token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

urlpatterns = format_suffix_patterns(urlpatterns)

