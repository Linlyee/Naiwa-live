import os
import imageio_ffmpeg
import subprocess

exe = imageio_ffmpeg.get_ffmpeg_exe()
VOICE_DIR = "douyin_live/assets/voice"
os.makedirs(VOICE_DIR, exist_ok=True)

# 1. From nailong_archive.mp3 (官方档案纯享版)
archive_mp3 = "nailong_archive.mp3"
slices_archive = {
    'intro.mp3': (0.30, 1.70, "我是奶龙！"),
    'bloat.mp3': (11.80, 15.90, "我的大肚肚真的很酷酷！"),
    'revive.mp3': (11.80, 15.90, "我的大肚肚真的很酷酷！"),
    'hungry.mp3': (23.85, 27.60, "求求你了，我想要好多好吃的！"),
    'sleep.mp3': (23.85, 27.60, "求求你了，我想要好多好吃的！"),
    'boing.mp3': (16.90, 22.95, "耶，帅的代名词就是我耶，胜利了！"),
    'dance.mp3': (16.90, 20.10, "耶，帅的代名词就是我耶！"),
    'song.mp3': (16.90, 20.10, "耶，帅的代名词就是我耶！"),
    'bubbles.mp3': (21.00, 22.95, "胜利了！"),
    'shiver.mp3': (4.85, 8.45, "你以为我会怕你吗？我根本不害怕的！"),
    'squish.mp3': (9.10, 11.10, "哼，你们给我等着！"),
    'blush.mp3': (2.40, 4.20, "哼，小熊！"),
}

for filename, (start, end, label) in slices_archive.items():
    dur = end - start
    out_file = os.path.join(VOICE_DIR, filename)
    cmd = [
        exe, '-ss', str(start), '-t', str(dur),
        '-i', archive_mp3,
        '-acodec', 'copy',
        out_file, '-y'
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated {filename}: {label} ({round(dur, 2)}s)")

# 2. From nailong_audio.mp3 (奶龙魔性八级狂笑，用于嘉年华与暴击)
laugh_mp3 = "nailong_audio.mp3"
gold_out = os.path.join(VOICE_DIR, "gold.mp3")
cmd_gold = [
    exe, '-ss', '0.0', '-t', '3.8',
    '-i', laugh_mp3,
    '-acodec', 'copy',
    gold_out, '-y'
]
subprocess.run(cmd_gold, check=True)
print("Generated gold.mp3: 奶龙魔性八级狂笑 (3.8s)")

# 3. Hearts (爱到埋住): 帅的代名词就是我耶
hearts_out = os.path.join(VOICE_DIR, "hearts.mp3")
cmd_hearts = [
    exe, '-ss', '16.90', '-t', '6.05',
    '-i', archive_mp3,
    '-acodec', 'copy',
    hearts_out, '-y'
]
subprocess.run(cmd_hearts, check=True)
print("Generated hearts.mp3: 耶，帅的代名词就是我耶，胜利了！ (6.05s)")

print("\nALL 100% OFFICIAL NAILONG VOICE SLICES CREATED!")
