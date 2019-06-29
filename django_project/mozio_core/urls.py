"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

#
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect
from django.views.i18n import JavaScriptCatalog
from django.conf.urls import handler400, handler403, handler404, handler500

from rest_framework.documentation import include_docs_urls
from provider.api_urls import urlpatterns as urlpatterns_api


js_info_dict = {
   'domain': 'django',
   'packages': None,
}

urlpatterns = [
    url(r'^$', lambda r: HttpResponseRedirect('api/docs/')),
    url(r'^api/', include(urlpatterns_api)),
    url(r'^site-admin/', admin.site.urls),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
]


try:
    from mozio_base.urls import urlpatterns as base_urlpatterns
    urlpatterns += base_urlpatterns
except ImportError:
    pass


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^debug/', include(debug_toolbar.urls)),
    ] + urlpatterns

    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
