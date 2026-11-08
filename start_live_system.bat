@echo off
chcp 936 >nul
cd /d "%~dp0"
title 奶娃AI直播 - 一键全系统自动启动
color 0A

echo ========================================================
echo       奶娃AI直播 - 全系统一键启动 (硬件级音频隔离版)
echo ========================================================
echo.

echo [1/4] 启动直播交互核心网关与画板服务 (Port 12393, 8088)...
powershell -Command "$p12393 = Get-NetTCPConnection -LocalPort 12393 -ErrorAction SilentlyContinue; if (!$p12393) { Start-Process python -ArgumentList 'douyin_live/live_bridge_server.py' -WorkingDirectory '%~dp0' -WindowStyle Hidden }"
powershell -Command "$p8088 = Get-NetTCPConnection -LocalPort 8088 -ErrorAction SilentlyContinue; if (!$p8088) { Start-Process python -ArgumentList 'douyin_live/start_live_preview.py' -WorkingDirectory '%~dp0' -WindowStyle Hidden }"
timeout /t 1 >nul

echo [2/4] 启动抖音弹幕抓手...
tasklist /fi "imagename eq BarrageGrab.exe" 2>nul | find /i "BarrageGrab.exe" >nul
if errorlevel 1 (
    if exist "%~dp0barrage_grab\启动弹幕抓手.bat" (
        start "抖音实时弹幕抓手" cmd /c "%~dp0barrage_grab\启动弹幕抓手.bat"
    )
) else (
    echo   [√] 弹幕抓手已在运行中。
)

echo [3/4] 检查抖音直播伴侣...
if exist "D:\zhibo\zhibobanlv\webcast_mate\直播伴侣 Launcher.exe" (
    start "" "D:\zhibo\zhibobanlv\webcast_mate\直播伴侣 Launcher.exe"
)

echo [4/4] 启动奶娃独立直播窗口...
set EDGE_ARGS=--app="http://localhost:8088/index.html" --use-fake-ui-for-media-stream --autoplay-policy=no-user-gesture-required --unsafely-treat-insecure-origin-as-secure="http://localhost:8088" --user-data-dir="%~dp0edge_profile" --disable-backgrounding-occluded-windows --disable-renderer-backgrounding --disable-background-timer-throttling --disable-features=CalculateNativeWinOcclusion,IntensiveWakeUpThrottling

if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" goto LAUNCH_X86
if exist "C:\Program Files\Microsoft\Edge\Application\msedge.exe" goto LAUNCH_PROG
start "" msedge %EDGE_ARGS%
goto LAUNCH_DONE

:LAUNCH_X86
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" %EDGE_ARGS%
goto LAUNCH_DONE

:LAUNCH_PROG
start "" "C:\Program Files\Microsoft\Edge\Application\msedge.exe" %EDGE_ARGS%
goto LAUNCH_DONE

:LAUNCH_DONE

echo.
echo ========================================================
echo   [OK] 全系统一键启动完成！
echo.
echo   【弹幕与音频状态】：
echo   1. 弹幕抓手：已读取 config.json 自动启动
echo   2. 音频分流：建议在【声音控制面板】中将 CABLE 侦听到耳机
echo   3. 奶娃系统：画板已就绪，伴奏与原唱点歌已就绪
echo ========================================================
echo.
timeout /t 5 >nul
