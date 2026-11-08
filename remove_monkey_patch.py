# -*- coding: utf-8 -*-
with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

old_redundant = """    // 弹幕识别中加入点歌检测
    const origHandleDanmaku = handleDanmakuCommand;
    handleDanmakuCommand = function(user, text) {
      const t = text.trim();
      if (t.includes('插队') || t.includes('为你点亮')) {
        handleSongRequest(t, user, true);
        return;
      }
      if (t.startsWith('点歌') || t.startsWith('播放') || t.startsWith('想听')) {
        handleSongRequest(t, user, false);
        return;
      }
      origHandleDanmaku(user, text);
    };"""

c = c.replace(old_redundant, "// 弹幕点歌已直接整合进核心 handleDanmakuCommand 引擎")

with open('douyin_live/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Removed redundant monkey patch!")
