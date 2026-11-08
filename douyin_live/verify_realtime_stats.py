# -*- coding: utf-8 -*-
import sys
import time
import json
import urllib.request
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=== 正在验证实时数据计费、收益与Token动态追踪系统 ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1080, "height": 1920})
    
    page.goto("http://localhost:8088/index.html", wait_until="networkidle")
    page.wait_for_timeout(2000)

    # 1. 确保初始数据重置为0 (测试开播纯净状态)
    page.evaluate("resetLiveStats()")
    page.wait_for_timeout(500)

    init_income = page.locator("#val-income").inner_text()
    init_tokens = page.locator("#val-tokens").inner_text()
    init_bowls = page.locator("#val-bowls").inner_text()
    init_vip = page.locator("#vip-name").inner_text()

    print(f"1. 开播初始状态: 收益={init_income}, Token={init_tokens}, 白饭={init_bowls}, 榜一={init_vip}")
    assert "0.00" in init_income, f"初始收益应为0，实际为: {init_income}"
    assert "0" in init_tokens, f"初始Token应为0，实际为: {init_tokens}"
    assert "虚位以待" in init_vip, f"初始榜一应为虚位以待，实际为: {init_vip}"

    # 2. 模拟观众送出【为你点亮 x 2】(9抖币*2 = 18抖币 = 1.8元, 1.8碗*2 = 3.6碗)
    print("2. 模拟送礼: 榜一大哥 送出【为你点亮】x2 (价值18抖币/¥1.80)")
    req_gift = urllib.request.Request(
        "http://localhost:12393/api/gift",
        data=json.dumps({"user": "榜一大哥", "gift": "为你点亮", "count": 2}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    urllib.request.urlopen(req_gift, timeout=5)
    page.wait_for_timeout(1500)

    updated_income = page.locator("#val-income").inner_text()
    updated_bowls = page.locator("#val-bowls").inner_text()
    updated_vip = page.locator("#vip-name").inner_text()
    print(f"送礼后看板: 收益={updated_income}, 白饭={updated_bowls}, 榜一={updated_vip}")
    assert "1.80" in updated_income, f"收益计算不符: {updated_income}"
    assert "3.6" in updated_bowls, f"白饭碗数不符: {updated_bowls}"
    assert "榜一大哥" in updated_vip, f"榜一姓名不符: {updated_vip}"

    # 3. 模拟观众发弹幕触发 Gemini AI
    print("3. 模拟观众发弹幕触发 Gemini，测试实际 Token 消耗实时累加...")
    req_chat = urllib.request.Request(
        "http://localhost:12393/api/danmaku",
        data=json.dumps({"user": "小迷妹", "danmaku": "奶娃你可以夸夸我吗"}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    urllib.request.urlopen(req_chat, timeout=5)
    
    # 等待 Gemini 回复并刷新 Token
    token_updated = False
    new_tokens = ""
    for _ in range(25):
        page.wait_for_timeout(200)
        curr_tokens = page.locator("#val-tokens").inner_text().strip()
        if curr_tokens != "0":
            new_tokens = curr_tokens
            token_updated = True
            break
            
    speech_text = page.locator("#speech-text").inner_text().strip()
    print(f"AI回复: \"{speech_text}\" | 消耗Token: {new_tokens}")
    assert token_updated, "Token消耗未能实时累加到顶部看板！"

    # 4. 截图保存验证产物
    shot_path = r"C:\Users\林夏\.gemini\antigravity-cli\brain\ca7952b9-cf9e-4d43-83dc-3bdc35eccb54\17_live_realtime_stats.png"
    page.screenshot(path=shot_path)
    print(f"4. 实时看板验证截图已保存至: {shot_path}")

    browser.close()

print("=== 实时收益与Token追踪系统 100% 验证通过！===")
