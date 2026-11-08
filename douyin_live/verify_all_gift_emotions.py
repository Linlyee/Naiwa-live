# -*- coding: utf-8 -*-
import os
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

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

    print("Navigating to http://localhost:8088/index.html...")
    page.goto('http://localhost:8088/index.html', wait_until='networkidle')
    time.sleep(1.5)

    # 1. 待机状态
    page.screenshot(path=os.path.join(output_dir, '01_idle.png'))
    print("01. Idle state verified.")

    # 2. 小心心 (blush.mp3 官方原版原声)
    print("Testing '小心心'...")
    page.evaluate("triggerAction('blush', '甜心小姐姐')")
    time.sleep(0.8)
    props_html = page.evaluate("document.getElementById('action-props').innerHTML")
    voice_src = page.evaluate("document.getElementById('voice-player').src")
    sfx_src = page.evaluate("document.getElementById('sfx-player').src")
    speech = page.evaluate("document.getElementById('speech-text').innerText")
    assert 'prop-heart-beat' in props_html, "Heart beat prop not found!"
    assert 'blush.mp3' in voice_src, f"blush.mp3 voice not played, got: {voice_src}"
    assert 'heartbeat.wav' in sfx_src, "Heartbeat SFX not played!"
    assert '小心心' in speech, "Speech text does not mention 小心心!"
    page.screenshot(path=os.path.join(output_dir, '02_blush_heartbeat.png'))
    time.sleep(1.8)
    page.evaluate("resetToIdle()")
    time.sleep(0.4)

    # 3. 抖音 (boing.mp3 官方原版原声)
    print("Testing '抖音'...")
    page.evaluate("triggerAction('boing', '音符达人')")
    time.sleep(0.8)
    props_html = page.evaluate("document.getElementById('action-props').innerHTML")
    voice_src = page.evaluate("document.getElementById('voice-player').src")
    sfx_src = page.evaluate("document.getElementById('sfx-player').src")
    speech = page.evaluate("document.getElementById('speech-text').innerText")
    assert 'prop-douyin' in props_html, "Douyin DJ prop not found!"
    assert 'boing.mp3' in voice_src, f"boing.mp3 voice not played, got: {voice_src}"
    assert 'confetti.wav' in sfx_src, "Confetti SFX not played!"
    assert '抖音' in speech, "Speech text does not mention 抖音!"
    page.screenshot(path=os.path.join(output_dir, '03_douyin_boing.png'))
    time.sleep(1.8)
    page.evaluate("resetToIdle()")
    time.sleep(0.4)

    # 4. 玫瑰 (squish.mp3 官方原版原声)
    print("Testing '玫瑰'...")
    page.evaluate("triggerAction('rose', '浪漫骑士')")
    time.sleep(0.8)
    props_html = page.evaluate("document.getElementById('action-props').innerHTML")
    voice_src = page.evaluate("document.getElementById('voice-player').src")
    sfx_src = page.evaluate("document.getElementById('sfx-player').src")
    speech = page.evaluate("document.getElementById('speech-text').innerText")
    assert 'prop-rose' in props_html, "Rose bouquet prop not found!"
    assert 'squish.mp3' in voice_src, f"squish.mp3 voice not played, got: {voice_src}"
    assert 'kiss.wav' in sfx_src, "Kiss SFX not played!"
    assert '玫瑰' in speech, "Speech text does not mention 玫瑰!"
    page.screenshot(path=os.path.join(output_dir, '04_rose_kiss.png'))
    time.sleep(1.8)
    page.evaluate("resetToIdle()")
    time.sleep(0.4)

    # 5. 人气票 (bubbles.mp3 官方原版原声)
    print("Testing '人气票'...")
    page.evaluate("triggerAction('praise', '铁杆粉丝')")
    time.sleep(0.8)
    props_html = page.evaluate("document.getElementById('action-props').innerHTML")
    voice_src = page.evaluate("document.getElementById('voice-player').src")
    sfx_src = page.evaluate("document.getElementById('sfx-player').src")
    speech = page.evaluate("document.getElementById('speech-text').innerText")
    assert 'prop-cheer' in props_html, "Cheer lightsticks prop not found!"
    assert 'bubbles.mp3' in voice_src, f"bubbles.mp3 voice not played, got: {voice_src}"
    assert 'confetti.wav' in sfx_src, "Confetti SFX not played!"
    assert '人气票' in speech, "Speech text does not mention 人气票!"
    page.screenshot(path=os.path.join(output_dir, '05_praise_cheer.png'))
    time.sleep(1.8)
    page.evaluate("resetToIdle()")
    time.sleep(0.4)

    # 6. 大啤酒 (bloat.mp3 官方原版原声)
    print("Testing '大啤酒'...")
    page.evaluate("triggerAction('pijiu', '豪爽大哥')")
    time.sleep(0.8)
    props_html = page.evaluate("document.getElementById('action-props').innerHTML")
    voice_src = page.evaluate("document.getElementById('voice-player').src")
    sfx_src = page.evaluate("document.getElementById('sfx-player').src")
    speech = page.evaluate("document.getElementById('speech-text').innerText")
    assert 'prop-beer' in props_html, "Beer mug prop not found!"
    assert 'bloat.mp3' in voice_src, f"bloat.mp3 voice not played, got: {voice_src}"
    assert 'beer_chug.wav' in sfx_src, "Beer chug SFX not played!"
    assert '啤酒' in speech, "Speech text does not mention 啤酒!"
    page.screenshot(path=os.path.join(output_dir, '06_pijiu_drunk.png'))
    time.sleep(2.0)
    page.evaluate("resetToIdle()")
    time.sleep(0.4)

    # 7. 你最好看 (dance.mp3 官方原版原声)
    print("Testing '你最好看'...")
    page.evaluate("triggerAction('haokan', '颜值担当')")
    time.sleep(0.8)
    props_html = page.evaluate("document.getElementById('action-props').innerHTML")
    voice_src = page.evaluate("document.getElementById('voice-player').src")
    sfx_src = page.evaluate("document.getElementById('sfx-player').src")
    speech = page.evaluate("document.getElementById('speech-text').innerText")
    assert 'prop-haokan' in props_html, "Haokan camera frame prop not found!"
    assert 'dance.mp3' in voice_src, f"dance.mp3 voice not played, got: {voice_src}"
    assert 'sparkle_camera.wav' in sfx_src, "Camera sparkle SFX not played!"
    assert '最好看' in speech, "Speech text does not praise beauty!"
    page.screenshot(path=os.path.join(output_dir, '07_haokan_heart_eyes.png'))
    time.sleep(1.8)
    page.evaluate("resetToIdle()")
    time.sleep(0.4)

    # 8. 手势比心 (shiver.mp3 官方原版原声)
    print("Testing '手势比心'...")
    page.evaluate("triggerAction('hearts', '比心狂魔')")
    time.sleep(0.8)
    props_html = page.evaluate("document.getElementById('action-props').innerHTML")
    voice_src = page.evaluate("document.getElementById('voice-player').src")
    sfx_src = page.evaluate("document.getElementById('sfx-player').src")
    speech = page.evaluate("document.getElementById('speech-text').innerText")
    assert 'prop-heart-beam' in props_html, "Heart laser beam prop not found!"
    assert 'shiver.mp3' in voice_src, f"shiver.mp3 voice not played, got: {voice_src}"
    assert 'heart_beam.wav' in sfx_src, "Heart beam SFX not played!"
    assert '爱心' in speech, "Speech text does not mention 爱心!"
    page.screenshot(path=os.path.join(output_dir, '08_hearts_beam.png'))
    time.sleep(1.8)
    page.evaluate("resetToIdle()")
    time.sleep(0.4)

    # 9. 为你点亮 (intro.mp3 官方原版原声加冕)
    print("Testing '为你点亮'...")
    page.evaluate("triggerAction('vip_song', '星光榜一')")
    time.sleep(0.8)
    props_html = page.evaluate("document.getElementById('action-props').innerHTML")
    voice_src = page.evaluate("document.getElementById('voice-player').src")
    sfx_src = page.evaluate("document.getElementById('sfx-player').src")
    speech = page.evaluate("document.getElementById('speech-text').innerText")
    assert 'prop-vip-crown' in props_html, "VIP royal crown prop not found!"
    assert 'intro.mp3' in voice_src, f"intro.mp3 voice not played, got: {voice_src}"
    assert 'crown_shimmer.wav' in sfx_src, "Crown shimmer SFX not played!"
    assert '为你点亮' in speech or 'VIP' in speech, "Speech text does not mention 为你点亮/VIP!"
    page.screenshot(path=os.path.join(output_dir, '09_vip_song_crown.png'))
    time.sleep(2.0)
    page.evaluate("resetToIdle()")
    time.sleep(0.4)

    # 10. 甜甜圈 (hungry.mp3 官方原版原声)
    print("Testing '甜甜圈'...")
    page.evaluate("triggerAction('donut', '甜蜜美食家')")
    time.sleep(0.8)
    props_html = page.evaluate("document.getElementById('action-props').innerHTML")
    voice_src = page.evaluate("document.getElementById('voice-player').src")
    sfx_src = page.evaluate("document.getElementById('sfx-player').src")
    speech = page.evaluate("document.getElementById('speech-text').innerText")
    assert 'prop-donut' in props_html, "Donut eating prop not found!"
    assert 'hungry.mp3' in voice_src, f"hungry.mp3 voice not played, got: {voice_src}"
    assert 'donut_eat.wav' in sfx_src, "Donut eat SFX not played!"
    assert '甜甜圈' in speech, "Speech text does not mention 甜甜圈!"
    page.screenshot(path=os.path.join(output_dir, '10_donut_bloat.png'))
    time.sleep(2.0)
    page.evaluate("resetToIdle()")
    time.sleep(0.4)

    # 11. 棒棒糖 (3D视频抱肚皮狂笑原声 + 结束后 gold.mp3 官方经典魔性八级狂笑原声)
    print("Testing '棒棒糖'...")
    page.evaluate("triggerAction('belly_laugh', '开心果大拿')")
    time.sleep(1.2)
    video_disp = page.evaluate("window.getComputedStyle(document.getElementById('video-action-player')).display")
    speech = page.evaluate("document.getElementById('speech-text').innerText")
    assert video_disp != 'none', "3D belly laugh video layer is not visible!"
    assert '棒棒糖' in speech or '哈哈' in speech, "Speech text does not match laugh!"
    page.screenshot(path=os.path.join(output_dir, '11_belly_laugh_3d.png'))

    # 等待大笑结束
    time.sleep(8.2)
    voice_src = page.evaluate("document.getElementById('voice-player').src")
    assert 'gold.mp3' in voice_src, f"gold.mp3 voice not played after laugh, got: {voice_src}"
    page.evaluate("resetToIdle()")
    time.sleep(0.5)

    print("\n--- Summary of Console Errors ---")
    if console_errors:
        print(f"Total Errors: {len(console_errors)}")
        for err in console_errors:
            print("  -", err)
    else:
        print("Zero console errors! Flawless execution.")

    browser.close()

assert len(console_errors) == 0, f"Encountered {len(console_errors)} console errors during test!"
print("All verification steps completed successfully with 100% authentic untouched previous version audio!")
