from django import forms
from .models import Score


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = [
            "title",
            "artist",
            "pdf_file",
            "audio_file",
        ]  # Include audio file field
