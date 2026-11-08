# -*- coding: utf-8 -*-
with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("playNaiwaAudio(ACTION_VOICES.song, `哇！感谢【${user}】送出【为你点亮】！", "playNaiwaAudio('assets/voice/gifts/gift_vip.mp3', `哇！感谢【${user}】送出【为你点亮】！")
c = c.replace("playNaiwaAudio(ACTION_VOICES.song, `收到【${user}】的VIP指定歌单！", "playNaiwaAudio('assets/voice/gifts/gift_vip.mp3', `收到【${user}】的VIP指定歌单！")

with open('douyin_live/index.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)

print("Updated danmaku VIP voices successfully!")
