from django.urls import path
from . import views

app_name = "pv3"  # 名前空間を追加

urlpatterns = [
    path("", views.index, name="index"),  # ホームページとして `index` ビューを設定
    path("upload/", views.upload_score, name="upload_score"),
    path("scores/", views.score_list, name="score_list"),
    path("scores/<int:score_id>/", views.view_score, name="view_score"),
    path(
        "scores/<int:score_id>/update/", views.update_score, name="update_score"
    ),  # 楽譜編集ビューを追加
    path(
        "scores/<int:score_id>/delete/", views.delete_score, name="delete_score"
    ),  # 楽譜削除ビューを追加
    path(
        "scores/<int:score_id>/edit_times/",
        views.edit_page_start_times,
        name="edit_page_start_times",
    ),  # ページ開始時間編集ビューを追加
]
