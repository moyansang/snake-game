@echo off
chcp 65001 >nul
title 贪吃蛇 - Git 初始化 & 上传 GitHub
cd /d "%~dp0"

echo ================================
echo   贪吃蛇 - Git 上传工具
echo ================================
echo.

:: === 检查 Git ===
echo [1/6] 检查 Git...
set "GIT=C:\Users\moyan\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe"
if not exist "%GIT%" (
    where git >nul 2>&1
    if errorlevel 1 (
        echo 错误: 未找到 Git，请先安装 Git: https://git-scm.com/
        pause
        exit /b 1
    )
    set "GIT=git"
)
echo 找到 Git ✓

:: === 初始化仓库(如未初始化) ===
echo.
echo [2/6] 初始化 Git 仓库...
if not exist ".git" (
    "%GIT%" init
    echo 仓库已初始化 ✓
) else (
    echo 仓库已存在 ✓
)

:: === 添加文件 ===
echo.
echo [3/6] 添加文件...
"%GIT%" add .
echo 文件已添加 ✓

:: === 提交 ===
echo.
echo [4/6] 提交更改...
"%GIT%" commit -m "feat: 贪吃蛇游戏 - 主菜单、倒计时、存档、音效、设置"
echo 已提交 ✓

:: === 检查 GitHub CLI ===
echo.
echo [5/6] 检查 GitHub CLI...
where gh >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠ 未安装 GitHub CLI (gh)
    echo.
    echo 请选择以下方式之一上传:
    echo.
    echo 方式一: 安装 gh CLI
    echo   1. 访问 https://cli.github.com/ 下载安装
    echo   2. 运行: gh auth login
    echo   3. 重新运行本脚本
    echo.
    echo 方式二: 手动上传
    echo   1. 在 GitHub 上创建仓库: snake-game
    echo   2. 运行以下命令:
    echo      git remote add origin https://github.com/moyansang/snake-game.git
    echo      git branch -M main
    echo      git push -u origin main
    echo.
    pause
    exit /b 0
)

:: === 创建 GitHub 仓库并推送 ===
echo.
echo [6/6] 创建 GitHub 仓库并推送...

:: 检查是否已登录
gh auth status >nul 2>&1
if errorlevel 1 (
    echo 请先登录 GitHub:
    echo   gh auth login
    pause
    exit /b 1
)

:: 创建仓库
gh repo create moyansang/snake-game --public --source=. --remote=origin --push 2>nul
if errorlevel 1 (
    :: 仓库可能已存在, 尝试直接推送
    "%GIT%" remote add origin https://github.com/moyansang/snake-game.git 2>nul
    "%GIT%" branch -M main
    "%GIT%" push -u origin main
)

echo.
echo ================================
echo   ✓ 上传完成!
echo   仓库地址: https://github.com/moyansang/snake-game
echo ================================
echo.
pause
