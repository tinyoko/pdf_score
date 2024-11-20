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


class PageStartTimeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        num_pages = kwargs.pop("num_pages", 0)
        page_start_times = kwargs.pop("page_start_times", {})
        super().__init__(*args, **kwargs)

        for page in range(1, num_pages + 1):
            field_name = f"page_{page}_start_time"
            self.fields[field_name] = forms.IntegerField(
                required=False,
                label=f"Page {page} Start Time (seconds)",
                initial=page_start_times.get(page, None),
                help_text="このページの開始時間を秒で指定してください",
            )
