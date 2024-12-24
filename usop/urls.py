# ruff: noqa
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from viewflow.contrib.auth import AuthViewset 
from viewflow.urls import Application, Site, ModelViewset
from django.views.generic.base import TemplateView

from .apps.services import views as ServiceViews
from .views import health, ready

site = Site(
    title="USOP", 
    viewsets=[
        *ServiceViews.viewsets
    ]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('health/', health),
    path('ready/', ready),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", TemplateView.as_view(template_name="index.html")),
    # path('', site.urls),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
