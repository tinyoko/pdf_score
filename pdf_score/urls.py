from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("pv3/", include("pv3.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
