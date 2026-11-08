@echo off
chcp 936 >nul
cd /d "%~dp0"
title 正在打开 QQ 音乐官方网页版...

set "EDGE_PATH=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE_PATH%" (
    set "EDGE_PATH=C:\Program Files\Microsoft\Edge\Application\msedge.exe"
)

set EDGE_ARGS=--app="https://y.qq.com" --user-data-dir="%~dp0edge_profile"

echo ========================================================
echo          QQ 音乐官方网页版 (独立应用窗口)
echo ========================================================
echo.
echo [提示] 窗口打开后：
echo 1. 点击右上角【登录】，使用微信扫码或 QQ 扫码登录您的账号/绿钻VIP
echo 2. 登录状态会自动保存在直播专属配置中，无需每次重复扫码
echo 3. 搜索或播放任意歌单，声音将直接流入抖音直播间！
echo.

if not exist "%EDGE_PATH%" (
    start https://y.qq.com
) else (
    start "" "%EDGE_PATH%" %EDGE_ARGS%
)

exit
