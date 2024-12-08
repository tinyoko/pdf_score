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
        ]


class PageStartTimeForm(forms.Form):
    def __init__(
        self,
        *args,
        num_pages=None,
        page_start_times=None,
        audio_duration=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.num_pages = num_pages
        self.audio_duration = audio_duration

        # Initialize default start times
        start_times = [0] * num_pages
        if audio_duration and num_pages:
            interval = audio_duration / (num_pages - 1)
            for i in range(1, num_pages):
                start_times[i] = start_times[i - 1] + interval

        # Set form fields
        for i in range(1, num_pages + 1):
            default_value = (
                page_start_times.get(str(i), start_times[i - 1])
                if page_start_times
                else start_times[i - 1]
            )
            self.fields[f"page_{i}"] = forms.FloatField(
                initial=default_value,
                label=f"Page {i} Start Time",
                required=False,
                min_value=0,
            )

    def clean(self):
        cleaned_data = super().clean()
        prev_time = None
        for i in range(1, self.num_pages + 1):
            key = f"page_{i}"
            if key in cleaned_data:
                current_time = cleaned_data[key]
                if i == 1 and current_time != 0:
                    raise forms.ValidationError(
                        "\u6700\u521d\u306e\u30da\u30fc\u30b8\u306e\u958b\u59cb\u6642\u9593\u306f0\u3067\u306a\u3051\u308c\u3070\u306a\u308a\u307e\u305b\u3093\u3002"
                    )
                if prev_time is not None and current_time < prev_time:
                    raise forms.ValidationError(
                        "\u5c0f\u3055\u3044\u30da\u30fc\u30b8\u756a\u53f7\u306e\u958b\u59cb\u6642\u9593\u306f\u5927\u304d\u3044\u30da\u30fc\u30b8\u756a\u53f7\u306e\u958b\u59cb\u6642\u9593\u3088\u308a\u5927\u304d\u304f\u3057\u3066\u304f\u3060\u3055\u3044\u3002"
                    )
                prev_time = current_time
