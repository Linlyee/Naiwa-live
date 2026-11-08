# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import urllib.request
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

output_dir = 'douyin_live/test_screenshots'
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={'width': 1080, 'height': 1920},
        device_scale_factor=1
    )
    page = context.new_page()

    console_errors = []
    def handle_msg(msg):
        if msg.type == 'error':
            txt = msg.text
            if '12393' in txt or 'ERR_CONNECTION_REFUSED' in txt:
                return
            console_errors.append(txt)

    page.on('console', handle_msg)
    page.on('pageerror', lambda exc: console_errors.append(str(exc)))

    print("1. Opening http://localhost:8088/index.html...")
    page.goto('http://localhost:8088/index.html', wait_until='networkidle')
    time.sleep(1.5)

    # 验证 WebSocket 状态变为已连接
    ws_status = page.evaluate("() => document.getElementById('ws-status').innerText")
    print(f"WS Status Badge: {ws_status}")
    assert '已成功连接' in ws_status, f"WebSocket did not connect, got: {ws_status}"

    # 2. 模拟真实外部送礼通过 HTTP/WS 网关推入 (大啤酒)
    print("2. Pushing gift '大啤酒' via bridge API...")
    req_data = json.dumps({"user": "榜一老哥", "gift": "大啤酒", "count": 1}).encode('utf-8')
    req = urllib.request.Request("http://localhost:12393/api/gift", data=req_data, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)

    time.sleep(0.8)
    props_html = page.evaluate("() => document.getElementById('action-props').innerHTML")
    speech = page.evaluate("() => document.getElementById('speech-text').innerText")
    assert 'prop-beer' in props_html, "Beer prop not shown from bridge!"
    assert '啤酒' in speech, "Speech text not triggered by bridge gift!"
    page.screenshot(path=os.path.join(output_dir, '12_bridge_gift_beer.png'))
    print("Bridge gift trigger verified!")

    time.sleep(2.0)
    page.evaluate("() => resetToIdle()")
    time.sleep(0.5)

    # 3. 模拟真实外部弹幕点歌通过 HTTP/WS 网关推入
    print("3. Pushing danmaku '点歌 稻香' via bridge API...")
    danmaku_data = json.dumps({"user": "音乐发烧友", "danmaku": "点歌 稻香"}).encode('utf-8')
    req2 = urllib.request.Request("http://localhost:12393/api/danmaku", data=danmaku_data, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req2)

    time.sleep(1.0)
    music_title_text = page.evaluate("() => document.getElementById('music-title').innerText")
    print(f"Music Title in UI: {music_title_text}")
    assert '稻香' in music_title_text, f"Song 稻香 not loaded into player, got: {music_title_text}"
    page.screenshot(path=os.path.join(output_dir, '13_bridge_song_request.png'))
    print("Bridge danmaku song request verified!")

    time.sleep(1.0)
    page.evaluate("() => resetToIdle()")
    time.sleep(0.5)

    # 4. 模拟为你点亮 VIP 霸权插队送礼推入
    print("4. Pushing VIP gift '为你点亮' via bridge API...")
    vip_data = json.dumps({"user": "超级皇帝", "gift": "为你点亮", "count": 1}).encode('utf-8')
    req3 = urllib.request.Request("http://localhost:12393/api/gift", data=vip_data, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req3)

    time.sleep(0.8)
    props_vip = page.evaluate("() => document.getElementById('action-props').innerHTML")
    assert 'royal-crown' in props_vip or 'prop-vip-crown' in props_vip, f"Crown prop not shown from bridge VIP gift, got: {props_vip}"
    page.screenshot(path=os.path.join(output_dir, '14_bridge_vip_crown.png'))
    print("Bridge VIP gift verified!")

    time.sleep(2.0)
    print("\n--- Summary of Console Errors ---")
    if console_errors:
        print(f"Total Errors: {len(console_errors)}")
        for err in console_errors:
            print("  -", err)
    else:
        print("Zero console errors! Flawless execution.")

    browser.close()

assert len(console_errors) == 0, f"Encountered {len(console_errors)} console errors!"
print("\nALL LIVE BRIDGE TESTS PASSED 100%!")
