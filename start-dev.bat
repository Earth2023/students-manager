@echo off
chcp 65001 >nul
cd /d "%~dp0"

set REPO_URL=https://github.com/Earth2023/students-manager.git
set GIT_CMD=git -c http.sslVerify=false

echo ================================================
echo  学生信息管理系统 — 开发模式
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
echo [1/2] 启动后端 (uvicorn --reload) ...
start "backend" cmd /c "cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 18765"

echo [2/2] 启动前端 (Vite dev server) ...
start "frontend" cmd /c "cd web && npm run dev"

echo.
echo 后端: http://127.0.0.1:18765
echo 前端: http://127.0.0.1:5173
echo API:  http://127.0.0.1:18765/docs
echo.
echo 请分别关闭后端/前端窗口来停止服务。
pause
