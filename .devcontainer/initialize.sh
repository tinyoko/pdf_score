#!/bin/bash
set -e # エラーが発生したらスクリプトを終了

# スクリプトのディレクトリからの相対パスでプロジェクトルートを決定
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${PROJECT_ROOT}/.env"
# devcontainer.json から参照しやすいように、シンボリックリンクは .devcontainer ディレクトリ内に作成
SELECTED_COMPOSE_FILE_SYMLINK="${PROJECT_ROOT}/.devcontainer/docker-compose.selected.yml"
# デフォルトで使用するComposeファイル (プロジェクトルートからの相対パス)
DEFAULT_COMPOSE_FILE_BASENAME="docker-compose.dev.yml"
DEFAULT_COMPOSE_FILE_PATH="${PROJECT_ROOT}/${DEFAULT_COMPOSE_FILE_BASENAME}"

COMPOSE_FILE_TO_USE="${DEFAULT_COMPOSE_FILE_PATH}" # デフォルト値

if [ -f "${ENV_FILE}" ]; then
    # .env ファイルから DEV_CONTAINER_COMPOSE_FILE を読み込む
    LINE=$(grep '^DEV_CONTAINER_COMPOSE_FILE=' "${ENV_FILE}" || true)
    if [ -n "$LINE" ]; then
        VALUE=$(echo "$LINE" | cut -d '=' -f2- | xargs) # xargsで前後の空白を除去
        if [ -n "$VALUE" ]; then
            CANDIDATE_FILE="${PROJECT_ROOT}/${VALUE}"
            if [ -f "${CANDIDATE_FILE}" ]; then
                COMPOSE_FILE_TO_USE="${CANDIDATE_FILE}"
                echo "Using compose file from .env: ${VALUE}"
            else
                echo "Warning: DEV_CONTAINER_COMPOSE_FILE in .env ('${VALUE}') does not exist. Using default: ${DEFAULT_COMPOSE_FILE_BASENAME}"
            fi
        else
            echo "Warning: DEV_CONTAINER_COMPOSE_FILE in .env is empty. Using default: ${DEFAULT_COMPOSE_FILE_BASENAME}"
        fi
    else
        echo "DEV_CONTAINER_COMPOSE_FILE not found in .env. Using default: ${DEFAULT_COMPOSE_FILE_BASENAME}"
    fi
else
    echo ".env file not found at ${ENV_FILE}. Using default compose file: ${DEFAULT_COMPOSE_FILE_BASENAME}"
fi

# 既存のシンボリックリンクやファイルがあれば削除
if [ -L "${SELECTED_COMPOSE_FILE_SYMLINK}" ] || [ -e "${SELECTED_COMPOSE_FILE_SYMLINK}" ]; then
    rm -f "${SELECTED_COMPOSE_FILE_SYMLINK}"
fi

# シンボリックリンクを作成
# ln -s <TARGET_ABSOLUTE_PATH> <LINK_NAME_ABSOLUTE_PATH>
ln -s "${COMPOSE_FILE_TO_USE}" "${SELECTED_COMPOSE_FILE_SYMLINK}"
echo "Symlinked ${COMPOSE_FILE_TO_USE} to ${SELECTED_COMPOSE_FILE_SYMLINK}"