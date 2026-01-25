@echo off
chcp 65001 >nul
echo ================================
echo   AIDocGenius Web 服务启动
echo ================================
echo.
echo 正在启动服务，请稍候...
echo 服务将在 http://localhost:8000 运行
echo 按 Ctrl+C 可以停止服务
echo.
python app.py
pause
