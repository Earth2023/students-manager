#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "================================================"
echo "  学生信息管理系统 — 开发模式"
echo "================================================"
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
