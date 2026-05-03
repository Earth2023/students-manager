#!/bin/bash
set -e

REPO_URL="https://github.com/Earth2023/students-manager.git"
APP_DIR="students-manager"
GIT_CMD="git -c http.sslVerify=false"

echo "================================================"
echo "  学生信息管理系统 — 开发模式"
echo "================================================"
echo ""

if [ ! -d "$APP_DIR" ]; then
    echo "正在从远程仓库拉取代码 ..."
    $GIT_CMD clone "$REPO_URL" "$APP_DIR"
else
    echo "正在更新代码 ..."
    $GIT_CMD -C "$APP_DIR" pull
fi

cd "$APP_DIR"

echo ""
echo "[1/2] 启动后端 (uvicorn --reload) ..."
(cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 18765) &

echo "[2/2] 启动前端 (Vite dev server) ..."
(cd web && npm run dev) &

echo ""
echo "后端: http://127.0.0.1:18765"
echo "前端: http://127.0.0.1:5173"
echo "API:  http://127.0.0.1:18765/docs"
echo ""

wait
