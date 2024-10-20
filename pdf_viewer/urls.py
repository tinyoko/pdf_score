from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.index, name="index"
    ),  # /pdf_viewer/ にアクセス時に views.index を呼び出す
]
