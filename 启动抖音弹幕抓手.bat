@echo off
chcp 936 >nul
cd /d "%~dp0barrage_grab"
title 抖音实时弹幕抓手 (BarrageGrab)
color 0B

:: 注入 .NET 8.0 x86 运行时环境路径
set "PATH=C:\Program Files (x86)\dotnet;%PATH%"
set "DOTNET_ROOT(x86)=C:\Program Files (x86)\dotnet"
set "DOTNET_ROOT=C:\Program Files (x86)\dotnet"

echo ========================================================
echo       抖音实时弹幕抓取控制台 (BarrageGrab)
echo ========================================================
echo.
echo   [提示] 正在从 config.json 读取配置并启动...
echo.
echo --------------------------------------------------------
echo   正在自动启动抓手并实时监听直播间弹幕...
echo   (开播后，所有观众弹幕、点赞、礼物都会在此窗口实时滚动显示)
echo   (请保持此控制台窗口开启，可最小化到任务栏)
echo --------------------------------------------------------
echo.
BarrageGrab.exe --config config.json
if %errorlevel% neq 0 (
    echo.
    echo --------------------------------------------------------
    echo 提示: 抓手退出，按任意键重新启动...
    echo --------------------------------------------------------
    pause >nul
)
