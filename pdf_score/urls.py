from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "pdf_viewer/", include("pdf_viewer.urls")
    ),  # /pdf_viewer で pdf_viewer アプリの URL をインクルード
]
