from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Score(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to="scores/")
    audio_file = models.FileField(
        upload_to="audio_tracks/", null=True, blank=True
    )  # New field for audio

    def __str__(self):
        return f"{self.title} by {self.artist}"


@receiver(post_delete, sender=Score)
def delete_file_on_model_delete(sender, instance, **kwargs):
    if instance.pdf_file:
        instance.pdf_file.delete(False)
    if instance.audio_file:  # Delete audio file if present
        instance.audio_file.delete(False)