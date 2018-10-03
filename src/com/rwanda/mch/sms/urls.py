from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls.defaults import *
from rapidsms.backends.kannel.views import KannelBackendView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r"^backend/kannel-smpp/$",
        KannelBackendView.as_view(backend_name="kannel-smpp")),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
