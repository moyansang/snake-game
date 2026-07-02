@echo off
chcp 65001 >nul
cd /d "%~dp0"
title 贪吃蛇

set "PYTHON_PATH=C:\Users\moyan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if exist "%PYTHON_PATH%" (
    start "" /D "%~dp0" "%PYTHON_PATH%" "%~dp0snake_game.py"
) else (
    echo 正在寻找 Python...
    start "" /D "%~dp0" python "%~dp0snake_game.py"
)
