# -*- coding: utf-8 -*-
import os
import time
from playwright.sync_api import sync_playwright

def verify_vip_song():
    os.makedirs('douyin_live/screenshots', exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1080, 'height': 1920})
        page = context.new_page()

        print("Navigating to http://localhost:8088/index.html...")
        page.goto('http://localhost:8088/index.html', wait_until='networkidle')
        page.wait_for_timeout(1500)

        # 触发 为你点亮 (VIP 插队点歌)
        print("Triggering 为你点亮 VIP 插队点歌...")
        page.locator('.action-tag[title*="为你点亮"]').click()
        page.wait_for_timeout(1200)

        # 截图：验证 VIP 插队横幅、点歌台 VIP 徽章与漂浮动画
        page.screenshot(path='douyin_live/screenshots/05_vip_song_request.png')
        print("Captured 05_vip_song_request.png")

        # 验证点歌台是否成功切换为 VIP 插队歌曲
        music_title = page.locator('#music-title').inner_html()
        assert "VIP插队" in music_title, "Error: VIP插队 badge not in music title!"

        browser.close()
        print("VIP Song Request test passed successfully!")

if __name__ == '__main__':
    verify_vip_song()
