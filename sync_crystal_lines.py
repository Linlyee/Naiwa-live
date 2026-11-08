with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = [
    (
        "playNaiwaAudio(ACTION_VOICES.boing, `收到【${user}】的抖音专属音符！动次打次，跟着奶娃一起摇摆起来吧！`, true);",
        "playNaiwaAudio(ACTION_VOICES.boing, `收到【${user}】的抖音专属音符啦！跟着动感节奏，和奶娃一起开心地摇摆起来吧！`, true);"
    ),
    (
        "playNaiwaAudio(ACTION_VOICES.rose, `哇！好香的红玫瑰！啵唧，送给【${user}】一个超级甜蜜的飞吻哦！`, true);",
        "playNaiwaAudio(ACTION_VOICES.rose, `哇！好香美丽的红玫瑰！送给【${user}】一个超级甜蜜的大飞吻哦！`, true);"
    ),
    (
        "playNaiwaAudio(ACTION_VOICES.pijiu, `哈，好爽快的大啤酒！吨吨吨，嗝，谢谢【${user}】大哥喝饱饱啦！`, true);",
        "playNaiwaAudio(ACTION_VOICES.pijiu, `哈！好爽快的一大杯冰啤酒！咕嘟咕嘟喝饱饱，嗝，谢谢【${user}】大哥飘飘然啦！`, true);"
    ),
    (
        "playNaiwaAudio(ACTION_VOICES.donut, `嗷呜！好甜好香的甜甜圈！【${user}】喂饱饱啦，肚皮变得圆滚滚像个大皮球啦！`, true);",
        "playNaiwaAudio(ACTION_VOICES.donut, `哇呜！好甜好香的甜甜圈！【${user}】喂饱饱大口吃掉啦，肚皮变得圆滚滚像个大皮球！`, true);"
    ),
    (
        "playNaiwaAudio(ACTION_VOICES.lollipop, `呼……笑得我肚皮好酸呀～谢谢【${user}】送的甜蜜棒棒糖，奶娃开心到飞起啦！`);",
        "playNaiwaAudio(ACTION_VOICES.lollipop, `哈哈哈哈！哎呀妈呀！棒棒糖太逗了，谢谢【${user}】，笑得我肚皮都抽筋啦！`);"
    )
]

for old, new in replacements:
    if old in text:
        text = text.replace(old, new)
        print("Updated speech line:", old[:30])
    else:
        print("Not found:", old[:30])

with open('douyin_live/index.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

print("index.html subtitle sync complete!")
