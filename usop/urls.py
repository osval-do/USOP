# ruff: noqa
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from viewflow.contrib.auth import AuthViewset 
from viewflow.urls import Application, Site, ModelViewset

from .apps.services import views as ServiceViews

site = Site(
    title="USOP", 
    viewsets=[
        *ServiceViews.viewsets
    ]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', site.urls),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
