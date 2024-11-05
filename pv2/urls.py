from django.urls import path
from . import views

app_name = "pv2"  # 名前空間を追加

urlpatterns = [
    path("", views.index, name="index"),  # ホームページとして `index` ビューを設定
    path("upload/", views.upload_score, name="upload_score"),
    path("scores/", views.score_list, name="score_list"),
    path("scores/<int:score_id>/", views.view_score, name="view_score"),
]
