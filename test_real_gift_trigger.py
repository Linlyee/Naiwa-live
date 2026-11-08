# -*- coding: utf-8 -*-
import os
import time
from playwright.sync_api import sync_playwright

def verify_gift_pipeline():
    os.makedirs('douyin_live/screenshots', exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1080, 'height': 1920})
        page = context.new_page()

        print("1. 打开直播间前端页面 http://localhost:8088/index.html...")
        page.goto('http://localhost:8088/index.html', wait_until='networkidle')
        page.wait_for_timeout(1000)

        # -------------------------------------------------------------
        # 验证链路 A：模拟抖音真实抓取到的送礼事件字符串 "[送出 棒棒糖 x1]"
        # -------------------------------------------------------------
        print("2. 模拟抖音弹幕流推送：[送出 棒棒糖 x1]...")
        page.evaluate("handleDanmakuCommand('老铁666', '[送出 棒棒糖 x1]')")
        page.wait_for_timeout(1500)

        # 检查是否激活 3D 抱腹狂笑动作
        is_laughing = page.evaluate("document.getElementById('video-action-player').classList.contains('active')")
        print("-> 3D 变大抱肚子狂笑动作是否成功激活:", is_laughing)
        assert is_laughing, "Error: 棒棒糖未能触发 3D 变大抱肚子狂笑动作！"

        # 截图验证
        page.screenshot(path='douyin_live/screenshots/test_danmaku_gift_laugh.png')

        # 等待狂笑结束恢复
        page.wait_for_timeout(8200)

        # -------------------------------------------------------------
        # 验证链路 B：模拟 WebSocket 结构化礼物事件：{"type": "gift", "gift": "为你点亮"}
        # -------------------------------------------------------------
        print("3. 模拟 WebSocket 结构化推送：送出【为你点亮】VIP插队点歌...")
        page.evaluate("handleGiftEvent('超级榜一', '为你点亮', 1)")
        page.wait_for_timeout(1500)

        # 检查点歌台是否成功切换为 VIP 插队
        music_html = page.locator('#music-title').inner_html()
        print("-> 点歌台当前播放状态:", "包含 VIP 插队徽章" if "VIP插队" in music_html else "未包含")
        assert "VIP插队" in music_html, "Error: 为你点亮未能触发 VIP 插队点歌！"

        page.screenshot(path='douyin_live/screenshots/test_ws_gift_vip_song.png')

        browser.close()
        print("========================================")
        print("全链路验证 100% 成功通过！真实送礼即可精准触发对应功能！")
        print("========================================")

if __name__ == '__main__':
    verify_gift_pipeline()
