# -*- coding: utf-8 -*-
with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = """        // 视听大动效反馈：星光升空漂浮 + 音符金光粒子爆发 + 亲口语音欢呼感谢
        playNaiwaAudio(ACTION_VOICES.song, `哇！收到【为你点亮】啦！感谢${userName}开启VIP专属通道，已立刻插队播放《${cleanName}》～`, true);"""

replacement = """        // 视听大动效反馈：星光升空漂浮 + 音符金光粒子爆发 + 亲口语音欢呼感谢
        playSFX('assets/sfx/crown_shimmer.wav');
        setAtmosphere('gold-vip-mode', 2800);
        playNaiwaAudio(ACTION_VOICES.song, `哇！收到【为你点亮】啦！感谢${userName}开启VIP专属通道，已立刻插队播放《${cleanName}》～`, true);"""

if target in c:
    c = c.replace(target, replacement)
    print("Successfully added playSFX and setAtmosphere to handleSongRequest VIP branch.")
else:
    print("Target not found directly.")

with open('douyin_live/index.html', 'w', encoding='utf-8') as f:
    f.write(c)
