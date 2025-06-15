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
ARG USER_UID=1001 # 1000から変更
ARG USER_GID=1001 # 1000から変更 (USER_UIDと合わせるのが一般的)

# グループ作成の堅牢化:
# 1. GID ${USER_GID} がどのグループにも使用されていなければ、グループ ${USERNAME} を GID ${USER_GID} で作成します。
# 2. GID ${USER_GID} が既にグループ ${USERNAME} によって使用されていれば、何もしません。
# 3. GID ${USER_GID} がグループ ${USERNAME} 以外のグループによって使用されていれば、エラー終了します。
RUN if ! getent group "${USER_GID}" > /dev/null; then \
        echo "Info: GID ${USER_GID} is free. Creating group '${USERNAME}' with GID ${USER_GID}." ; \
        groupadd --gid "${USER_GID}" "${USERNAME}"; \
    elif [ "$(getent group "${USER_GID}" | cut -d: -f1)" = "${USERNAME}" ]; then \
        echo "Info: Group '${USERNAME}' with GID ${USER_GID} already exists. No action needed for group." ; \
    else \
        echo "Error: GID ${USER_GID} is already in use by group '$(getent group "${USER_GID}" | cut -d: -f1)' (expected '${USERNAME}'). Cannot proceed." >&2; \
        exit 1; \
    fi
# ユーザー作成とsudo設定の堅牢化 (同様のロジックを適用)
RUN export DEBIAN_FRONTEND=noninteractive && \
    if ! getent passwd "${USER_UID}" > /dev/null; then \
        echo "Info: UID ${USER_UID} is free. Creating user '${USERNAME}' with UID ${USER_UID}." ; \
        useradd --uid "${USER_UID}" --gid "${USER_GID}" -m "${USERNAME}"; \
    elif [ "$(getent passwd "${USER_UID}" | cut -d: -f1)" = "${USERNAME}" ]; then \
        echo "Info: User '${USERNAME}' with UID ${USER_UID} already exists. No action needed for user." ; \
    else \
        echo "Error: UID ${USER_UID} is already in use by user '$(getent passwd "${USER_UID}" | cut -d: -f1)' (expected '${USERNAME}'). Cannot proceed." >&2; \
        exit 1; \
    fi \
    # (オプション) sudoをパスワードなしで実行できるようにする (開発時に便利)
    && apt-get update && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# 作業ディレクトリと仮想環境の所有権を新しいユーザーに変更
# /code ディレクトリ全体と、その中のファイルに対する所有権を vscode ユーザーに設定し、書き込み権限を付与
RUN chown -R $USERNAME:$USER_GID /code /opt/venv && chmod -R u+w /code

# ユーザーを切り替え
USER $USERNAME

# デフォルトコマンド
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pdf_score.wsgi:application"]
