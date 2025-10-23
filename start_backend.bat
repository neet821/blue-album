@echo off
echo ========================================
echo 启动后端服务
echo ========================================
cd /d d:\Laragon\laragon\www\blue-local
echo.
echo 当前目录: %CD%
echo.
echo 正在启动 Uvicorn 服务器...
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
