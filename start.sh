#!/bin/bash
set -e

REPO_URL="https://github.com/Earth2023/students-manager.git"
APP_DIR="students-manager"
GIT_CMD="git -c http.sslVerify=false"

echo "================================================"
echo "  学生信息管理系统 — 安装/启动器"
echo "================================================"
echo ""

if [ ! -d "$APP_DIR" ]; then
    echo "正在从远程仓库拉取代码 ..."
    $GIT_CMD clone "$REPO_URL" "$APP_DIR"
elif [ ! -d "$APP_DIR/.git" ]; then
    echo "目录不完整，重新拉取 ..."
    rm -rf "$APP_DIR"
    $GIT_CMD clone "$REPO_URL" "$APP_DIR"
else
    echo "正在更新代码 ..."
    $GIT_CMD -C "$APP_DIR" pull
fi

cd "$APP_DIR"

echo ""
echo "[1/3] 安装后端依赖 ..."
cd backend
pip install -r requirements.txt

echo "[2/3] 构建前端 ..."
cd ../web
npm install && npm run build

echo "[3/3] 启动服务 ..."
cd ../backend
echo ""
echo "服务已启动: http://127.0.0.1:18765"
echo "API 文档:  http://127.0.0.1:18765/docs"
echo ""
uvicorn app.main:app --host 0.0.0.0 --port 18765
