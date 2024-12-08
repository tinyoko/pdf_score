import mimetypes
from mutagen.mp3 import MP3
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from PyPDF2 import PdfReader


class Score(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to="scores/")
    audio_file = models.FileField(upload_to="audio_tracks/", null=True, blank=True)
    page_start_times = models.JSONField(
        default=dict,
        help_text="\u5404\u30da\u30fc\u30b8\u306e\u958b\u59cb\u6642\u9593（\u79d2\u5358\u4f4d）\u3092\u4fdd\u5b58\u3059\u308b\u8f9e\u66f8",
    )

    def __str__(self):
        return f"{self.title} by {self.artist}"

    def get_num_pages(self):
        reader = PdfReader(self.pdf_file)
        return len(reader.pages)

    def get_audio_duration(self):
        if not self.audio_file:
            return 0
        try:
            mime_type, _ = mimetypes.guess_type(self.audio_file.path)
            if mime_type == "audio/mpeg":
                audio = MP3(self.audio_file.path)
                return audio.info.length
            else:
                raise ValueError("Unsupported audio format")
        except Exception as e:
            # 非対応フォーマットの場合、再生時間を0として処理を続行
            return 0


@receiver(post_delete, sender=Score)
def delete_file_on_model_delete(sender, instance, **kwargs):
    if instance.pdf_file:
        instance.pdf_file.delete(False)
    if instance.audio_file:
        instance.audio_file.delete(False)
