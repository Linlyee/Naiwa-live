# -*- coding: utf-8 -*-
import os
import time
from playwright.sync_api import sync_playwright

def verify_closed_loop():
    os.makedirs('douyin_live/screenshots', exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1080, 'height': 1920})
        page = context.new_page()

        print("1. 导航到 http://localhost:8088/index.html...")
        page.goto('http://localhost:8088/index.html', wait_until='networkidle')
        page.wait_for_timeout(1500)

        # 验证 1：确认右下角推荐歌单卡片已彻底移除
        card_count = page.locator('.song-sheet-card').count()
        assert card_count == 0, "Error: 右下角推荐歌单卡片未被移除！"

        # 验证 2：确认底部点歌台明确显示“必须附带点歌二字”醒目标注
        tip_text = page.locator('.tip-rule').inner_text()
        assert "点歌" in tip_text and "二字" in tip_text, "Error: 点歌台未显示点歌二字提醒！"

        # 截图 1：全景界面确认（无右下角卡片，点歌台提醒清晰）
        page.screenshot(path='douyin_live/screenshots/10_rule_overview_clean.png')
        print("-> 截取 10_rule_overview_clean.png (全景界面已彻底移除右下角歌单卡片)")

        # 验证 3：观众不带“点歌”二字（例如发“孤勇者”或“怎么点歌”），触发规则提醒语音
        page.evaluate("handleDanmakuCommand('小迷糊', '孤勇者')")
        page.wait_for_timeout(800)

        speech = page.locator('#speech-text').inner_text()
        assert "点歌" in speech and "附带" in speech, "Error: 未触发附带点歌二字的规则提醒！"
        page.screenshot(path='douyin_live/screenshots/11_rule_voice_reminder.png')
        print("-> 截取 11_rule_voice_reminder.png (成功提醒观众必须附带点歌二字)")

        # 验证 4：观众规范发送「点歌 演员」成功点歌排队
        page.evaluate("handleDanmakuCommand('听歌达人', '点歌 演员')")
        page.wait_for_timeout(800)
        danmaku_last = page.locator('.danmaku-msg').last.inner_text()
        assert "演员" in danmaku_last, "Error: 规范点歌未能进入队列！"

        # 验证 5：送礼物【为你点亮】+ 附带“点歌”二字指定歌名 VIP 霸权插队
        page.evaluate("handleDanmakuCommand('榜一大哥', '[送出 为你点亮 x1]')")
        page.wait_for_timeout(1000)

        page.evaluate("handleDanmakuCommand('榜一大哥', '点歌 稻香')")
        page.wait_for_timeout(1000)

        music_html = page.locator('#music-title').inner_html()
        assert "稻香" in music_html, "Error: VIP指定歌曲《稻香》未成功切换！"
        assert "VIP插队" in music_html, "Error: 未打上 VIP插队 标记！"
        page.screenshot(path='douyin_live/screenshots/12_vip_song_with_rule.png')
        print("-> 截取 12_vip_song_with_rule.png (送礼人带“点歌”指定歌名VIP插队成功)")

        # 验证 6：10 分钟无人点歌空闲自动轮播热门歌曲
        page.evaluate("triggerAutoTrendingSong()")
        page.wait_for_timeout(800)
        music_req = page.locator('#music-requester').inner_text()
        assert "系统推荐" in music_req, "Error: 自动轮播未能成功启动！"

        browser.close()
        print("==================================================")
        print("全部闭环测试 100% 验证通过！完全符合要求！")
        print("==================================================")

if __name__ == '__main__':
    verify_closed_loop()
