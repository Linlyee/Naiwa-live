@echo off
cd /d "%~dp0"
title 正在打开抖音直播间独立窗口...

set "EDGE_PATH=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE_PATH%" (
    set "EDGE_PATH=C:\Program Files\Microsoft\Edge\Application\msedge.exe"
)

set EDGE_ARGS=--app="http://localhost:8088/index.html" --use-fake-ui-for-media-stream --autoplay-policy=no-user-gesture-required --unsafely-treat-insecure-origin-as-secure="http://localhost:8088" --user-data-dir="D:\zhibo\Open-LLM-VTuber\edge_profile" --disable-backgrounding-occluded-windows --disable-renderer-backgrounding --disable-background-timer-throttling --disable-features=CalculateNativeWinOcclusion,IntensiveWakeUpThrottling

if not exist "%EDGE_PATH%" (
    echo [提示] 未找到Edge绝对路径，正在调用默认浏览器打开...
    start http://localhost:8088/index.html
) else (
    echo [√] 正在以独立窗口模式打开直播间（自动记忆上次窗口大小）...
    start "" "%EDGE_PATH%" %EDGE_ARGS%
)

exit
