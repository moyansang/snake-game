@echo off
chcp 65001 >nul
title 贪吃蛇 - 打包工具
echo ================================
echo    贪吃蛇游戏 - 打包成 EXE
echo ================================
echo.

set "PYTHON_PATH=C:\Users\moyan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if exist "%PYTHON_PATH%" (
    echo [1/3] 检查 Python...
    "%PYTHON_PATH%" --version
) else (
    echo 错误: 找不到 Python, 尝试使用系统 Python...
    set "PYTHON_PATH=python"
)

echo.
echo [2/3] 安装 PyInstaller...
"%PYTHON_PATH%" -m pip install pyinstaller --quiet

echo.
echo [3/3] 打包生成 EXE...
"%PYTHON_PATH%" -m PyInstaller --onefile --windowed --name "贪吃蛇" snake_game.py

echo.
echo ================================
echo    打包完成!
echo    EXE 文件在 dist 文件夹中
echo ================================
echo.
pause
