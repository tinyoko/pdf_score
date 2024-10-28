from django.shortcuts import render, redirect, get_object_or_404
from .models import Score
from .forms import ScoreForm


# ホームページビュー
def index(request):
    return render(request, "pv2/index.html")


# 楽譜登録用のビュー
def upload_score(request):
    if request.method == "POST":
        form = ScoreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("score_list")
    else:
        form = ScoreForm()
    return render(request, "pv2/upload_score.html", {"form": form})


# 楽譜の一覧を表示するビュー
def score_list(request):
    scores = Score.objects.all()
    return render(request, "pv2/score_list.html", {"scores": scores})


# 楽譜を表示するビュー
def view_score(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    return render(request, "pv2/view_score.html", {"score": score})
