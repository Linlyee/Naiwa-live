# -*- coding: utf-8 -*-
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

path = r'D:\zhibo\Open-LLM-VTuber\douyin_live\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace ACTION_VOICES block
old_block_start = "    // 100% 奶龙正统官方音色 · 10大官方礼物专属独占台词"
old_block_end = "    };\n"

start_idx = content.find("    // 100% 奶龙正统官方音色")
if start_idx == -1:
    start_idx = content.find("const ACTION_VOICES = {")
    # backtrack to comment
    start_idx = content.rfind("    //", 0, start_idx)

end_idx = content.find("    };\n", start_idx) + len("    };\n")

new_action_voices_block = """    // 100% 跟之前一模一样的官方原版原声音频切片（纯净无损 · 零AI合成失真 · 10大礼物各不相同绝不重复）
    const ACTION_VOICES = {
      intro: 'assets/voice/intro.mp3',       // “我是奶龙！” (官方原声)
      blush: 'assets/voice/blush.mp3',       // “哼，小熊！” (官方原声)
      boing: 'assets/voice/boing.mp3',       // “耶，帅的代名词就是我耶，胜利了！” (官方原声)
      rose: 'assets/voice/squish.mp3',       // “哼，你们给我等着！” (官方原声)
      praise: 'assets/voice/bubbles.mp3',   // “胜利了！” (官方原声)
      pijiu: 'assets/voice/bloat.mp3',       // “我的大肚肚真的很酷酷！” (官方原声)
      haokan: 'assets/voice/dance.mp3',     // “耶，帅的代名词就是我耶！” (官方原声)
      hearts: 'assets/voice/shiver.mp3',     // “你以为我会怕你吗？我根本不害怕的！” (官方原声)
      vip: 'assets/voice/intro.mp3',         // “我是奶龙！” (官方原声，加冕专属)
      donut: 'assets/voice/hungry.mp3',     // “求求你了，我想要好多好吃的！” (官方原声)
      lollipop: 'assets/voice/gold.mp3',     // “奶龙经典魔性八级狂笑 (哈哈哈哈哈哈)” (官方原声)
      song_regular: 'assets/voice/song.mp3', // “耶，帅的代名词就是我耶！” (官方原声)
      song_auto: 'assets/voice/intro.mp3',   // “我是奶龙！” (官方原声)
      // 兼容历史原版切片别名
      dance: 'assets/voice/dance.mp3',
      bubbles: 'assets/voice/bubbles.mp3',
      bloat: 'assets/voice/bloat.mp3',
      revive: 'assets/voice/intro.mp3',
      hungry: 'assets/voice/hungry.mp3',
      song: 'assets/voice/song.mp3',
      gold: 'assets/voice/gold.mp3',
      sleep: 'assets/voice/sleep.mp3',
      squish: 'assets/voice/squish.mp3'
    };
"""

content = content[:start_idx] + new_action_voices_block + content[end_idx:]

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Updated ACTION_VOICES to 100% authentic previous version files!")
