from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("pdf_viewer/", include("pdf_viewer.urls")),
    path("pv2/", include("pv2.urls")),
    path("pv3/", include("pv3.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
