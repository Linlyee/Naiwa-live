with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "playNaiwaAudio(ACTION_VOICES.revive, `哇！感谢【${user}】送出【为你点亮】！想指定歌曲请在公屏发送「点歌 歌名」（一定要带“点歌”二字哦），奶娃立刻为你插队换歌～`, true);",
    "playNaiwaAudio(ACTION_VOICES.vip, `哇！感谢【${user}】送出【为你点亮】！想指定歌曲请在公屏发送「点歌 歌名」（一定要带“点歌”二字哦），奶娃立刻为你插队换歌～`, true);"
)

text = text.replace(
    "playNaiwaAudio(ACTION_VOICES.revive, `收到【${user}】的VIP指定歌单！已立即插队为你切换到《${extracted}》！`, true);",
    "playNaiwaAudio(ACTION_VOICES.vip, `收到【${user}】的VIP指定歌单！已立即插队为你切换到《${extracted}》！`, true);"
)

text = text.replace(
    "playNaiwaAudio(ACTION_VOICES.song, `现在直播间空闲啦，奶娃为大家随机挑选了当下热门金曲《${pick.title}》！点歌要附带“点歌”二字哦，发送「点歌 歌名」就能排上你的歌啦～`);",
    "playNaiwaAudio(ACTION_VOICES.song_auto, `现在直播间空闲啦，奶娃为大家随机挑选了当下热门金曲《${pick.title}》！点歌要附带“点歌”二字哦，发送「点歌 歌名」就能排上你的歌啦～`);"
)

text = text.replace(
    "playNaiwaAudio(ACTION_VOICES.revive, `哇！收到【为你点亮】啦！感谢${userName}开启VIP专属通道，已立刻插队播放《${cleanName}》～`, true);",
    "playNaiwaAudio(ACTION_VOICES.vip, `哇！收到【为你点亮】啦！感谢${userName}开启VIP专属通道，已立刻插队播放《${cleanName}》～`, true);"
)

text = text.replace(
    "playNaiwaAudio(ACTION_VOICES.song, `好听好听！${userName}点的《${cleanName}》排上啦，马上给哥哥姐姐放～`);",
    "playNaiwaAudio(ACTION_VOICES.song_regular, `好听好听！${userName}点的《${cleanName}》排上啦，马上给哥哥姐姐放～`);"
)

with open('douyin_live/index.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

print("Song request lines updated!")
