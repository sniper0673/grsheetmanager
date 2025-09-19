#!/bin/bash

# --- 설정 영역 ---
BASE_DIR="/srv/stock/grsheetmanager"
SOURCE_DIR="$BASE_DIR/src"
PROGRAM_PY="mygrsheetmanager.gr_sheet_manager_server"   # -m 으로 실행할 모듈 경로
VENV_ACTIVATE="$BASE_DIR/venv/bin/activate"
PORT=6009
# PORT=6019 #백업서버
LOG_FILE_NAME="gr_sheet_manager.log"

# --- 로그 디렉토리 및 파일 설정 (선택) ---
LOG_DIR="$BASE_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$LOG_FILE_NAME"

# 기존 로그 파일 초기화 (파일은 유지, 내용만 삭제)
: > "$LOG_FILE"
echo "[INFO] 기존 로그 파일 초기화됨: $LOG_FILE"

# --- 가상환경 활성화 ---
if [ -f "$VENV_ACTIVATE" ]; then
    source "$VENV_ACTIVATE"
else
    echo "[ERROR] 가상환경 activate 파일이 존재하지 않습니다: $VENV_ACTIVATE"
    exit 1
fi

# --- 작업 디렉토리로 이동 ---
cd "$SOURCE_DIR" || {
    echo "[ERROR] 디렉토리 이동 실패: $SOURCE_DIR"
    exit 1
}

# --- PYTHONPATH 설정 ---
export PYTHONPATH="$SOURCE_DIR"

# --- 서버 실행 (백그라운드 실행, 로그 저장) ---
echo "[INFO] 서버를 시작합니다... ($PROGRAM_PY on port $PORT)"
nohup python -m waitress --port=$PORT --threads=4 "$PROGRAM_PY:app" >> "$LOG_FILE" 2>&1 &
echo "[INFO] 서버 실행됨. 로그: $LOG_FILE"