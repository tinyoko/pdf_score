from django.shortcuts import render, redirect, get_object_or_404
from .models import Score
from .forms import ScoreForm, PageStartTimeForm
from django.urls import reverse
from PyPDF2 import PdfReader
import json


# ホームページビュー
def index(request):
    return render(request, "pv3/index.html")


# 楽譜登録用のビュー
def upload_score(request):
    if request.method == "POST":
        form = ScoreForm(request.POST, request.FILES)
        if form.is_valid():
            score = form.save(commit=False)
            score.save()

            # PDFのページ数を取得し、各ページの開始時間をデフォルトで空の状態に設定
            reader = PdfReader(score.pdf_file)
            page_start_times = {i + 1: None for i in range(len(reader.pages))}
            score.page_start_times = page_start_times
            score.save()

            return redirect(reverse("pv3:score_list"))
    else:
        form = ScoreForm()
    return render(request, "pv3/upload_score.html", {"form": form})


# 楽譜の一覧を表示するビュー
def score_list(request):
    scores = Score.objects.all()
    return render(request, "pv3/score_list.html", {"scores": scores})


# 楽譜を表示するビュー
def view_score(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    return render(
        request,
        "pv3/view_score.html",
        {"score": score, "page_start_times": json.dumps(score.page_start_times)},
    )


# 楽譜編集用のビュー
def edit_score(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    if request.method == "POST":
        form = ScoreForm(request.POST, request.FILES, instance=score)
        if form.is_valid():
            score = form.save(commit=False)
            score.save()

            return redirect("pv3:score_list")
    else:
        form = ScoreForm(instance=score)
    return render(request, "pv3/upload_score.html", {"form": form})


# ページ開始時間編集用のビュー
def edit_page_start_times(request, score_id):
    score = get_object_or_404(Score, id=score_id)

    if request.method == "POST":
        form = PageStartTimeForm(
            request.POST,
            num_pages=score.get_num_pages(),
            page_start_times=score.page_start_times,
        )
        if form.is_valid():
            page_start_times = score.page_start_times or {}
            for key, value in form.cleaned_data.items():
                if value is not None:
                    page_number = int(key.split("_")[1])
                    page_start_times[page_number] = value
            score.page_start_times = page_start_times
            score.save()
            return redirect(reverse("pv3:edit_page_start_times", args=[score.id]))
    else:
        form = PageStartTimeForm(
            num_pages=score.get_num_pages(), page_start_times=score.page_start_times
        )

    # フォームの初期値を設定してレンダリング
    for key, value in score.page_start_times.items():
        if value is not None:
            form.fields[f"page_{key}_start_time"].initial = value

    return render(
        request, "pv3/edit_page_start_times.html", {"form": form, "score": score}
    )
