@echo off
chcp 65001 >nul
title 贪吃蛇

set "PYTHON_PATH=C:\Users\moyan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if exist "%PYTHON_PATH%" (
    start "" "%PYTHON_PATH%" "%~dp0snake_game.py"
) else (
    start "" python "%~dp0snake_game.py"
)
