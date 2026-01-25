@echo off
chcp 65001 >nul
echo ================================
echo   AIDocGenius 依赖安装
echo ================================
echo.
echo 正在安装所需依赖包...
pip install -r requirements.txt
echo.
echo ================================
echo   依赖安装完成！
echo ================================
pause
