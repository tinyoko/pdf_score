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

    # 非rootユーザーの作成
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # (オプション) sudoをパスワードなしで実行できるようにする (開発時に便利)
    && apt-get update && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# 作業ディレクトリと仮想環境の所有権を新しいユーザーに変更
RUN chown -R $USERNAME:$USER_GID /code /opt/venv

# ユーザーを切り替え
USER $USERNAME

# デフォルトコマンド
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pdf_score.wsgi:application"]