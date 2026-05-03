@echo off
chcp 65001 >nul
cd /d "%~dp0"

set REPO_URL=https://github.com/Earth2023/students-manager.git
set GIT_CMD=git -c http.sslVerify=false

echo ================================================
echo  学生信息管理系统 — 安装/启动器
echo ================================================
echo.

if exist ".git" (
    echo 正在更新代码 ...
    %GIT_CMD% pull
    if errorlevel 1 (
        echo 更新失败
        pause
        exit /b 1
    )
) else if exist "students-manager\.git" (
    cd students-manager
    echo 正在更新代码 ...
    %GIT_CMD% pull
    if errorlevel 1 (
        echo 更新失败
        pause
        exit /b 1
    )
) else (
    echo 正在从远程仓库拉取代码 ...
    %GIT_CMD% clone %REPO_URL% students-manager
    if errorlevel 1 (
        echo 拉取失败，请检查网络连接和 Git 安装
        pause
        exit /b 1
    )
    cd students-manager
)

echo.
echo [1/3] 安装后端依赖 ...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo 安装 Python 依赖失败
    pause
    exit /b 1
)

echo [2/3] 构建前端 ...
cd ../web
call npm install
if errorlevel 1 (
    echo 安装 Node 依赖失败
    pause
    exit /b 1
)
call npm run build
if errorlevel 1 (
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
