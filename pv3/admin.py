from django.contrib import admin
from .models import Score


class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "artist",
        "pdf_file",
        "audio_file",
        "display_page_start_times",
    )

    def display_page_start_times(self, obj):
        return obj.page_start_times

    display_page_start_times.short_description = "Page Start Times"


# Scoreモデルを管理画面に登録
admin.site.register(Score, ScoreAdmin)
