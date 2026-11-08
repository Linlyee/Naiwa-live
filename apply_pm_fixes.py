# -*- coding: utf-8 -*-
with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修复大礼物横幅跑道重叠：由 385px 下移到 405px，避开顶部免费口令条
content = content.replace(
    '#gift-toast-container {\n      position: absolute;\n      top: 385px;',
    '#gift-toast-container {\n      position: absolute;\n      top: 405px;'
)

# 2. 修复台词气泡框与弹幕标题重叠：台词框上移至 1295px，弹幕框微调
content = content.replace(
    '.speech-box {\n      position: absolute;\n      top: 1330px;',
    '.speech-box {\n      position: absolute;\n      top: 1295px;'
)

content = content.replace(
    '.danmaku-box {\n      position: absolute;\n      bottom: 210px;\n      left: 50px;\n      width: 580px;\n      height: 280px;',
    '.danmaku-box {\n      position: absolute;\n      bottom: 195px;\n      left: 50px;\n      width: 580px;\n      height: 255px;'
)

# 3. 优化棒棒糖标签为皇冠特技标识
content = content.replace(
    '<span class="coin-badge gold">9抖币·狂笑</span>',
    '<span class="coin-badge gold">👑 9抖币·狂笑</span>'
)

# 4. 优化大笑结束语音发声：让奶娃在恢复待机时用萌音亲口感谢
content = content.replace(
    "setSpeech('呼……笑得我肚皮好酸呀～谢谢哥哥姐姐送的棒棒糖！');\n            resetToIdle();",
    "playNaiwaAudio(ACTION_VOICES.bloat, '呼……笑得我肚皮好酸呀～谢谢哥哥姐姐送的棒棒糖！');\n            resetToIdle();"
)

# 5. 动作触发时立刻打断睡觉状态，瞬间唤醒
trigger_head = "    function triggerAction(action) {\n      if (isTalking) stopTalking();\n      if (currentActionTimeout) clearTimeout(currentActionTimeout);"
new_trigger_head = """    function triggerAction(action) {
      if (isTalking) stopTalking();
      if (currentActionTimeout) clearTimeout(currentActionTimeout);
      if (sleepBubble) sleepBubble.classList.remove('active');"""

content = content.replace(trigger_head, new_trigger_head)

with open('douyin_live/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied PM optimizations successfully!")
