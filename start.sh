#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "================================================"
echo "  学生信息管理系统 — 生产部署"
echo "================================================"
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
