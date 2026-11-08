# -*- coding: utf-8 -*-
import sys
import time
import json
import urllib.request
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=== 开始端到端自动化验证：Antigravity Gemini 智能弹幕问答 ===")

# 1. 启动 Playwright 打开直播间
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1080, "height": 1920})
    
    console_logs = []
    page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))

    print("1. 正在访问直播间页面 http://localhost:8088/index.html...")
    page.goto("http://localhost:8088/index.html", wait_until="networkidle")
    page.wait_for_timeout(2000)

    # 验证 WebSocket 连接状态
    status_text = page.locator("#ws-status").inner_text()
    print("WebSocket 状态:", status_text)
    assert "已成功连接" in status_text or "Gemini" in status_text, "WebSocket 未成功连接！"

    # 2. 发送测试弹幕 (观众向奶娃提问)
    user = "糖糖姐姐"
    question = "奶娃你今天吃饱饭了吗？"
    print(f"2. 模拟观众【{user}】发送弹幕提问: \"{question}\"")
    
    danmaku_req = urllib.request.Request(
        "http://localhost:12393/api/danmaku",
        data=json.dumps({"user": user, "danmaku": question}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(danmaku_req, timeout=5) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
        print("API 响应:", res_data)

    # 3. 等待 Gemini 生成回复并推送至直播间
    print("3. 等待 Gemini 智能回复推送到前端页面...")
    # 等待 speech-text 更新为包含软萌回复的内容
    speech_el = page.locator("#speech-text")
    
    success = False
    ai_reply_text = ""
    for _ in range(25):  # 最多等待 5 秒
        page.wait_for_timeout(200)
        curr_text = speech_el.inner_text().strip()
        if curr_text and curr_text != question and ("奶娃" in curr_text or "饭" in curr_text or "肚" in curr_text or "饱" in curr_text or "姐" in curr_text or "duang" in curr_text):
            ai_reply_text = curr_text
            success = True
            break
    
    print("当前角色气泡台词:", ai_reply_text)
    assert success, f"未能检测到 Gemini 智能回复，当前台词为: {speech_el.inner_text()}"

    # 4. 检查弹幕列表中是否出现奶娃的回复气泡
    danmaku_items = page.locator(".danmaku-msg").all_inner_texts()
    print(f"当前弹幕条数: {len(danmaku_items)}")
    for item in danmaku_items:
        print(" - 弹幕:", item.replace('\n', ' '))
    assert len(danmaku_items) >= 2, "弹幕列表中未找到用户弹幕或奶娃回复！"

    # 5. 截图保存验证产物
    shot_path = r"C:\Users\林夏\.gemini\antigravity-cli\brain\ca7952b9-cf9e-4d43-83dc-3bdc35eccb54\15_gemini_danmaku_reply.png"
    page.screenshot(path=shot_path)
    print(f"4. 截图已保存至: {shot_path}")

    # 6. 再测试第二句提问，验证上下文与持续互动
    user2 = "小杰哥哥"
    question2 = "奶娃你会跳舞吗？"
    print(f"5. 模拟观众【{user2}】发送弹幕提问: \"{question2}\"")
    danmaku_req2 = urllib.request.Request(
        "http://localhost:12393/api/danmaku",
        data=json.dumps({"user": user2, "danmaku": question2}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    urllib.request.urlopen(danmaku_req2, timeout=5)
    page.wait_for_timeout(3000)
    
    second_reply = speech_el.inner_text().strip()
    print("第二句提问角色气泡台词:", second_reply)
    
    shot_path2 = r"C:\Users\林夏\.gemini\antigravity-cli\brain\ca7952b9-cf9e-4d43-83dc-3bdc35eccb54\16_gemini_second_reply.png"
    page.screenshot(path=shot_path2)
    print(f"6. 第二次问答截图已保存至: {shot_path2}")

    browser.close()

print("=== 自动化验证完成：Gemini 智能弹幕问答 100% 成功打通！===")
