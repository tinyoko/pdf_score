# ベースイメージ
FROM ubuntu:24.04

# 環境変数を設定
ENV PYTHONUNBUFFERED=1

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev python3-venv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを作成
WORKDIR /code

# Pythonの仮想環境を作成
RUN python3 -m venv /opt/venv

# 仮想環境のPythonとpipを使用するようにPATHを設定
ENV PATH="/opt/venv/bin:$PATH"

# 要求パッケージを仮想環境内にインストール
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . /code/

# デフォルトコマンド
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pdf_score.wsgi:application"]