# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8088/index.html')
    page.wait_for_timeout(1000)

    # 1. 触发送出 为你点亮
    page.evaluate("handleDanmakuCommand('电竞老铁', '[送出 为你点亮 x1]')")
    page.wait_for_timeout(500)
    vip_cache = page.evaluate("JSON.stringify(pendingVipUsers)")
    print("Pending VIP Cache:", vip_cache)

    # 2. 触发弹幕 孤勇者
    page.evaluate("handleDanmakuCommand('电竞老铁', '孤勇者')")
    page.wait_for_timeout(500)

    html = page.locator('#music-title').inner_html()
    with open('test_output.txt', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved music title HTML to test_output.txt")
    browser.close()
