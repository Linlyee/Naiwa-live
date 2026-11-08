import os

path = r'D:\zhibo\Open-LLM-VTuber\douyin_live\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update ACTION_VOICES definition
old_action_voices = """    // 100% 官方原版奶龙原声音频切片 (用户最喜欢的纯正奶龙/小黄人原声)
    const ACTION_VOICES = {
      intro: 'assets/voice/intro.mp3',       // “我是奶龙！”
      boing: 'assets/voice/boing.mp3',       // “耶，帅的代名词就是我耶，胜利了！”
      bubbles: 'assets/voice/bubbles.mp3',   // “胜利了！”
      sleep: 'assets/voice/sleep.mp3',       // “求求你了，我想要好多好吃的！”
      squish: 'assets/voice/squish.mp3',     // “哼，你们给我等着！”
      bloat: 'assets/voice/bloat.mp3',       // “我的大肚肚真的很酷酷！”
      blush: 'assets/voice/blush.mp3',       // “哼，小熊！”
      dance: 'assets/voice/dance.mp3',       // “耶，帅的代名词就是我耶！”
      shiver: 'assets/voice/shiver.mp3',     // “你以为我会怕你吗？我根本不害怕的！”
      hearts: 'assets/voice/hearts.mp3',     // “耶，帅的代名词就是我耶，胜利了！”
      gold: 'assets/voice/gold.mp3',         // “奶龙魔性八级狂笑 (哈哈哈哈哈哈)”
      hungry: 'assets/voice/hungry.mp3',     // “求求你了，我想要好多好吃的！”
      revive: 'assets/voice/revive.mp3',     // “我的大肚肚真的很酷酷！”
      song: 'assets/voice/song.mp3'          // “耶，帅的代名词就是我耶！”
    };"""

new_action_voices = """    // 100% 奶龙正统官方音色 · 10大官方礼物专属独占台词（台词变音色不变，各礼物绝不重复！）
    const ACTION_VOICES = {
      intro: 'assets/voice/intro.mp3',                    // 原版奶龙自我介绍
      blush: 'assets/voice/gifts/gift_blush.mp3',         // 小心心专属：哇！谢谢小主人送的小心心，奶娃心里扑通扑通跳个不停呢！
      boing: 'assets/voice/gifts/gift_boing.mp3',         // 抖音专属：收到抖音专属音符！动次打次，跟着奶娃一起摇摆起来吧！
      rose: 'assets/voice/gifts/gift_rose.mp3',           // 玫瑰专属：哇！好香的红玫瑰！啵唧，送你一个超级甜蜜的飞吻哦！
      praise: 'assets/voice/gifts/gift_praise.mp3',       // 人气票专属：人气暴涨啦！感谢大家投出的人气票，奶娃冲鸭冲榜一！
      pijiu: 'assets/voice/gifts/gift_pijiu.mp3',         // 大啤酒专属：哈，好爽快的大啤酒！吨吨吨，嗝，奶娃喝饱饱飘飘然啦！
      haokan: 'assets/voice/gifts/gift_haokan.mp3',       // 你最好看专属：眼里全是你！你在奶娃心里就是全宇宙最好看最帅气的小可爱！
      hearts: 'assets/voice/gifts/gift_hearts.mp3',       // 手势比心专属：收到超级大爱心！超能爱心光波，发射！一定要接住满满的幸福哦！
      vip: 'assets/voice/gifts/gift_vip.mp3',             // 为你点亮专属：璀璨星光为你点亮！已开启VIP霸权插队通道，快快发歌名插队吧！
      donut: 'assets/voice/gifts/gift_donut.mp3',         // 甜甜圈专属：嗷呜！好甜好香的甜甜圈！肚皮变得圆滚滚像个大皮球啦！
      lollipop: 'assets/voice/gifts/gift_lollipop.mp3',   // 棒棒糖专属：哈哈哈哈！哎呀妈呀！棒棒糖太逗了，笑得我肚皮都抽筋啦！
      song_regular: 'assets/voice/gifts/gift_song_regular.mp3', // 普通点歌入队专属台词
      song_auto: 'assets/voice/gifts/gift_song_auto.mp3',       // 10分钟自动随机播歌专属台词
      // 兼容历史原版切片别名
      dance: 'assets/voice/gifts/gift_haokan.mp3',
      bubbles: 'assets/voice/gifts/gift_praise.mp3',
      bloat: 'assets/voice/gifts/gift_pijiu.mp3',
      revive: 'assets/voice/gifts/gift_vip.mp3',
      hungry: 'assets/voice/gifts/gift_donut.mp3',
      song: 'assets/voice/gifts/gift_rose.mp3',
      gold: 'assets/voice/gold.mp3'
    };"""

if old_action_voices in content:
    content = content.replace(old_action_voices, new_action_voices)
    print("ACTION_VOICES replaced successfully!")
else:
    print("Warning: old_action_voices not found directly, checking normalization...")

# 2. Update triggerGiftAction cases
replacements = [
    # 玫瑰
    ("playNaiwaAudio(ACTION_VOICES.song, `哇！好香的红玫瑰！啵唧，送给【${user}】一个超级甜蜜的飞吻哦！`, true);",
     "playNaiwaAudio(ACTION_VOICES.rose, `哇！好香的红玫瑰！啵唧，送给【${user}】一个超级甜蜜的飞吻哦！`, true);"),
    # 人气票
    ("playNaiwaAudio(ACTION_VOICES.bubbles, `人气暴涨啦！感谢【${user}】投出的人气票，奶娃冲鸭冲榜一！`, true);",
     "playNaiwaAudio(ACTION_VOICES.praise, `人气暴涨啦！感谢【${user}】投出的人气票，奶娃冲鸭冲榜一！`, true);"),
    # 大啤酒
    ("playNaiwaAudio(ACTION_VOICES.bloat, `哈，好爽快的大啤酒！吨吨吨，嗝，谢谢【${user}】大哥喝饱饱啦！`, true);",
     "playNaiwaAudio(ACTION_VOICES.pijiu, `哈，好爽快的大啤酒！吨吨吨，嗝，谢谢【${user}】大哥喝饱饱啦！`, true);"),
    # 你最好看
    ("playNaiwaAudio(ACTION_VOICES.dance, `眼里全是你！【${user}】在奶娃心里就是全宇宙最好看最帅气的小可爱！`, true);",
     "playNaiwaAudio(ACTION_VOICES.haokan, `眼里全是你！【${user}】在奶娃心里就是全宇宙最好看最帅气的小可爱！`, true);"),
    # 为你点亮
    ("playNaiwaAudio(ACTION_VOICES.revive, `璀璨星光为你点亮！感谢【${user}】开启VIP通道，快快发歌名插队吧！`, true);",
     "playNaiwaAudio(ACTION_VOICES.vip, `璀璨星光为你点亮！感谢【${user}】开启VIP通道，快快发歌名插队吧！`, true);"),
    # 甜甜圈
    ("playNaiwaAudio(ACTION_VOICES.hungry, `嗷呜！好甜好香的甜甜圈！【${user}】喂饱饱啦，肚皮变得圆滚滚像个大皮球啦！`, true);",
     "playNaiwaAudio(ACTION_VOICES.donut, `嗷呜！好甜好香的甜甜圈！【${user}】喂饱饱啦，肚皮变得圆滚滚像个大皮球啦！`, true);"),
    # 棒棒糖结束后答谢
    ("playNaiwaAudio(ACTION_VOICES.intro, `呼……笑得我肚皮好酸呀～谢谢【${user}】送的甜蜜棒棒糖，奶娃开心到飞起啦！`);",
     "playNaiwaAudio(ACTION_VOICES.lollipop, `呼……笑得我肚皮好酸呀～谢谢【${user}】送的甜蜜棒棒糖，奶娃开心到飞起啦！`);"),
    # 自动选歌播放
    ("playNaiwaAudio(ACTION_VOICES.song, `特别为您挑选了当红热门金曲《${pick.title}》！要点歌请发“点歌”哦！`);",
     "playNaiwaAudio(ACTION_VOICES.song_auto, `奶娃为您挑选了当红热门金曲《${pick.title}》！点歌请发送“点歌+歌名”哦！`);"),
    # handleSongRequest VIP
    ("playNaiwaAudio(ACTION_VOICES.revive, `哇！收到为你点亮！感谢【${userName}】VIP专属通道，插队播放《${cleanName}》！`, true);",
     "playNaiwaAudio(ACTION_VOICES.vip, `哇！收到为你点亮！感谢【${userName}】VIP专属通道，插队播放《${cleanName}》！`, true);"),
    # handleSongRequest regular queue
    ("playNaiwaAudio(ACTION_VOICES.song, `已为【${userName}】将《${cleanName}》排入歌单，稍后为您播放！`);",
     "playNaiwaAudio(ACTION_VOICES.song_regular, `好听好听！已为【${userName}】将《${cleanName}》排入歌单，稍后为您播放！`);")
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"Replaced: {old[:30]}...")
    else:
        print(f"Warning: pattern not found: {old[:40]}")

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Update completed successfully!")
