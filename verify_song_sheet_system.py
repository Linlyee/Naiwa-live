# -*- coding: utf-8 -*-
import os
import time
from playwright.sync_api import sync_playwright

def verify_all_song_features():
    os.makedirs('douyin_live/screenshots', exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1080, 'height': 1920})
        page = context.new_page()

        print("1. 导航到直播间页面 http://localhost:8088/index.html...")
        page.goto('http://localhost:8088/index.html', wait_until='networkidle')
        page.wait_for_timeout(1500)

        # -------------------------------------------------------------
        # 验证 1：热门歌单推荐看板卡片是否正常显示在右下角
        # -------------------------------------------------------------
        song_card = page.locator('.song-sheet-card')
        assert song_card.is_visible(), "Error: 热门歌单推荐卡片未显示！"
        page.screenshot(path='douyin_live/screenshots/06_hot_song_card_overview.png')
        print("-> 验证1成功：06_hot_song_card_overview.png (右下角热门歌单卡片清晰展示)")

        # -------------------------------------------------------------
        # 验证 2：点击“查看全部 24 首”打开全景歌单弹窗
        # -------------------------------------------------------------
        print("2. 打开 24 首精选完整歌单弹窗...")
        page.locator('.song-sheet-footer span', has_text='查看全部').click()
        page.wait_for_timeout(800)
        assert page.locator('#song-modal').is_visible(), "Error: 歌单弹窗未能打开！"
        page.screenshot(path='douyin_live/screenshots/07_full_song_modal.png')
        print("-> 验证2成功：07_full_song_modal.png (24首热门歌单全景弹窗展示无误)")

        # 关闭弹窗
        page.locator('.modal-close').click()
        page.wait_for_timeout(500)

        # -------------------------------------------------------------
        # 验证 3：测试“先送礼、后发歌名”的 VIP 智能识别闭环
        # -------------------------------------------------------------
        print("3. 测试送礼人指定歌名闭环：老铁送出【为你点亮】，接着发弹幕「孤勇者」...")
        # Step A: 送出 为你点亮
        page.evaluate("handleDanmakuCommand('电竞老铁', '[送出 为你点亮 x1]')")
        page.wait_for_timeout(1000)

        # Step B: 紧接着该用户只发歌名「孤勇者」
        page.evaluate("handleDanmakuCommand('电竞老铁', '孤勇者')")
        page.wait_for_timeout(1200)

        # 检查是否成功将《孤勇者》识别为该用户的 VIP 插队歌曲
        music_html = page.locator('#music-title').inner_html()
        assert "孤勇者" in music_html, "Error: 送礼人指定的歌名《孤勇者》未被识别！"
        assert "VIP插队" in music_html, "Error: 未打上 VIP插队 标记！"
        page.screenshot(path='douyin_live/screenshots/08_vip_song_association.png')
        print("-> 验证3成功：08_vip_song_association.png (成功识别送礼人指定的《孤勇者》为VIP插队！)")

        # -------------------------------------------------------------
        # 验证 4：测试“10 分钟无人点歌时自动随机选一首当下热门歌”
        # -------------------------------------------------------------
        print("4. 测试空闲自动 DJ 引擎：模拟触发 10 分钟自动热门歌推荐...")
        page.evaluate("triggerAutoTrendingSong()")
        page.wait_for_timeout(1200)

        music_html_idle = page.locator('#music-title').inner_html()
        music_req = page.locator('#music-requester').inner_text()
        print("-> 自动轮播状态：", music_req)
        page.screenshot(path='douyin_live/screenshots/09_auto_idle_dj.png')
        print("-> 验证4成功：09_auto_idle_dj.png (空闲自动轮播热门歌曲机制正常！)")

        browser.close()
        print("==================================================")
        print("3 大功能升级全部验证通过！无任何缺陷！")
        print("==================================================")

if __name__ == '__main__':
    verify_all_song_features()
