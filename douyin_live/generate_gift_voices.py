# -*- coding: utf-8 -*-
import os
import win32com.client
import soundfile as sf
import numpy as np
from scipy import signal

output_dir = 'douyin_live/assets/voice/gifts'
os.makedirs(output_dir, exist_ok=True)

voice = win32com.client.Dispatch("SAPI.SpVoice")
# 选取中文语音
for v in voice.GetVoices():
    if 'Huihui' in v.GetDescription() or 'Chinese' in v.GetDescription():
        voice.Voice = v
        break

voice.Rate = 1  # 语速适中偏快

GIFT_LINES = {
    'blush': ('gift_blush', '哇！谢谢小主人送的小心心，奶娃心里扑通扑通跳个不停呢！'),
    'boing': ('gift_boing', '收到抖音专属音符！动次打次，跟着奶娃一起摇摆起来吧！'),
    'rose': ('gift_rose', '哇！好香的红玫瑰！啵唧，送你一个超级甜蜜的飞吻哦！'),
    'praise': ('gift_praise', '人气暴涨啦！感谢大家投出的人气票，奶娃冲鸭冲榜一！'),
    'pijiu': ('gift_pijiu', '哈，好爽快的大啤酒！吨吨吨，嗝，奶娃喝饱饱飘飘然啦！'),
    'haokan': ('gift_haokan', '眼里全是你！你在奶娃心里就是全宇宙最好看最帅气的小可爱！'),
    'hearts': ('gift_hearts', '收到超级大爱心！超能爱心光波，发射！一定要接住满满的幸福哦！'),
    'vip': ('gift_vip', '璀璨星光为你点亮！已开启VIP霸权插队通道，快快发歌名插队吧！'),
    'donut': ('gift_donut', '嗷呜！好甜好香的甜甜圈！肚皮变得圆滚滚像个大皮球啦！'),
    'lollipop': ('gift_lollipop', '哈哈哈哈！哎呀妈呀！棒棒糖太逗了，笑得我肚皮都抽筋啦！')
}

def make_chibi_voice(input_path, output_path, speed_factor=1.28):
    data, sr = sf.read(input_path)
    # 重采样变调提速，转为清亮Q萌童音
    new_len = int(len(data) / speed_factor)
    chibi_data = signal.resample(data, new_len)
    chibi_data = np.tanh(chibi_data * 1.2) * 0.95
    sf.write(output_path, chibi_data, sr)

for key, (filename, text) in GIFT_LINES.items():
    raw_path = os.path.join(output_dir, f"{filename}_raw.wav")
    final_path = os.path.join(output_dir, f"{filename}.wav")
    mp3_path = os.path.join(output_dir, f"{filename}.mp3")

    stream = win32com.client.Dispatch("SAPI.SpFileStream")
    stream.Open(raw_path, 3) # SSFMCreateForWrite
    voice.AudioOutputStream = stream
    voice.Speak(text)
    stream.Close()

    make_chibi_voice(raw_path, final_path, speed_factor=1.26)
    
    # 写入 mp3
    data, sr = sf.read(final_path)
    sf.write(mp3_path, data, sr)

    if os.path.exists(raw_path):
        os.remove(raw_path)

    print(f"Generated {filename}.wav & .mp3: {text}")

print("All 10 gift voice lines generated successfully via SAPI!")
