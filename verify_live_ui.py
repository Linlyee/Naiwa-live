# -*- coding: utf-8 -*-
import os
import time
from playwright.sync_api import sync_playwright

def verify_live():
    os.makedirs('douyin_live/screenshots', exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1080, 'height': 1920})
        page = context.new_page()

        print("Navigating to http://localhost:8088/index.html...")
        page.goto('http://localhost:8088/index.html', wait_until='networkidle')
        page.wait_for_timeout(1500)

        # 截图 1：全景待机状态
        page.screenshot(path='douyin_live/screenshots/01_full_live_overview.png')
        print("Captured 01_full_live_overview.png")

        # 触发棒棒糖 (抱肚大笑)
        print("Clicking 棒棒糖 to trigger belly laugh...")
        page.locator('.action-tag.special-glow').click()
        page.wait_for_timeout(1500)

        # 截图 2：大笑播放中
        page.screenshot(path='douyin_live/screenshots/02_belly_laugh_active.png')
        print("Captured 02_belly_laugh_active.png")

        # 等待完整动作结束并恢复待机
        print("Waiting for belly laugh to finish and restore...")
        page.wait_for_timeout(8500)

        # 截图 3：恢复待机状态
        page.screenshot(path='douyin_live/screenshots/03_restored_idle.png')
        print("Captured 03_restored_idle.png")

        browser.close()
        print("All verifications completed cleanly!")

if __name__ == '__main__':
    verify_live()
