@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ================================================
echo  学生信息管理系统 — 生产部署
echo ================================================
echo.

echo [1/3] 安装后端依赖 ...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 安装 Python 依赖失败
    pause
    exit /b 1
)

echo [2/3] 构建前端 ...
cd ../web
call npm install
if %errorlevel% neq 0 (
    echo 安装 Node 依赖失败
    pause
    exit /b 1
)
call npm run build
if %errorlevel% neq 0 (
    echo 构建前端失败
    pause
    exit /b 1
)

echo [3/3] 启动服务 ...
cd ../backend
echo.
echo 服务已启动: http://127.0.0.1:18765
echo API 文档:  http://127.0.0.1:18765/docs
echo.
uvicorn app.main:app --host 0.0.0.0 --port 18765
