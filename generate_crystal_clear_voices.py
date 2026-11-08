# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import urllib.request
import imageio_ffmpeg
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

api_key = os.environ.get('SILICONFLOW_API_KEY', 'your-siliconflow-api-key')
url = 'https://api.siliconflow.cn/v1/audio/speech'
voice_uri = 'speech:nailong_pure_crystal:d80vfqecnncc73bibn1g:zawoltqvcsospxihbsdn'
out_dir = 'douyin_live/assets/voice/gifts'
os.makedirs(out_dir, exist_ok=True)
exe = imageio_ffmpeg.get_ffmpeg_exe()

scripts = {
    'gift_blush.mp3': '哇！谢谢小主人送的小心心，奶娃心里扑通扑通跳个不停呢！',
    'gift_boing.mp3': '收到抖音专属音符啦！跟着动感节奏，和奶娃一起开心地摇摆起来吧！',
    'gift_rose.mp3': '哇！好香美丽的红玫瑰！送你一个超级甜蜜的大飞吻哦！',
    'gift_praise.mp3': '人气暴涨啦！感谢大家投出的人气票，奶娃冲鸭冲榜一！',
    'gift_pijiu.mp3': '哈！好爽快的一大杯冰啤酒！咕嘟咕嘟喝饱饱，嗝，飘飘然啦！',
    'gift_haokan.mp3': '眼里全是你！你在奶娃心里就是全宇宙最好看最帅气的小可爱！',
    'gift_hearts.mp3': '收到超级大爱心！超能爱心光波，发射！一定要接住满满的幸福哦！',
    'gift_vip.mp3': '璀璨星光为你点亮！已开启VIP霸权插队通道，快快发歌名插队吧！',
    'gift_donut.mp3': '哇呜！好甜好香的甜甜圈！大口大口吃掉啦，肚皮变得圆滚滚像个大皮球！',
    'gift_lollipop.mp3': '哈哈哈哈！哎呀妈呀！棒棒糖太逗了，笑得我肚皮都抽筋啦！',
    'gift_song_regular.mp3': '好听好听！这首美妙的歌曲排上啦，马上放给大家听！',
    'gift_song_auto.mp3': '奶娃自动挑选了一首当下最热门的宝藏好歌放给大家听！'
}

for fname, text in scripts.items():
    raw_tmp = os.path.join(out_dir, f"raw_{fname}")
    final_target = os.path.join(out_dir, fname)
    print(f"Synthesizing {fname}...")
    
    data = {
        'model': 'FunAudioLLM/CosyVoice2-0.5B',
        'input': text,
        'voice': voice_uri,
        'response_format': 'mp3',
        'sample_rate': 32000,
        'speed': 1.02
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'),
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read()
        with open(raw_tmp, 'wb') as f:
            f.write(content)
    
    # Broadcast studio audio mastering filter:
    # 1. highpass=80Hz: remove sub-bass rumble/mud
    # 2. lowpass=11500Hz: remove ultrasonic distortion/aliasing
    # 3. afftdn=nf=-25: dynamic spectral denoise
    # 4. loudnorm: EBU R128 broadcast standard loudness normalization (punchy, crystal clear vocal)
    master_cmd = [
        exe, '-i', raw_tmp,
        '-af', 'highpass=f=80,lowpass=f=11500,afftdn=nf=-25,loudnorm=I=-15:TP=-1.5:LRA=9',
        '-ar', '44100', '-b:a', '192k',
        final_target, '-y'
    ]
    subprocess.run(master_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(raw_tmp):
        os.remove(raw_tmp)
    print(f"Mastered {fname} ({os.path.getsize(final_target)} bytes)")
    time.sleep(0.4)

print("\nAll 12 voice tracks synthesized and broadcast-mastered crystal clear!")
