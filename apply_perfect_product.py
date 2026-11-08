import re

with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS for .coin-badge, .action-tag, .action-icon-img, and special-glow
extra_css = """    .coin-badge {
      font-size: 14px;
      font-weight: 700;
      color: #ffd043;
      background: rgba(255, 208, 67, 0.15);
      border: 1px solid rgba(255, 208, 67, 0.35);
      border-radius: 12px;
      padding: 1px 7px;
      margin-left: 6px;
      display: inline-block;
      vertical-align: middle;
    }

    .coin-badge.gold {
      color: #ffffff;
      background: linear-gradient(135deg, #ff9800, #ff5722);
      border: 1px solid #ffb74d;
      box-shadow: 0 2px 10px rgba(255, 87, 34, 0.5);
    }

    .action-tag.special-glow {
      background: linear-gradient(135deg, rgba(255, 184, 0, 0.25), rgba(255, 82, 82, 0.22));
      border: 1.5px solid rgba(255, 208, 67, 0.85);
      box-shadow: 0 0 20px rgba(255, 184, 0, 0.45);
      animation: pulseGlow 2.5s infinite alternate;
    }

    @keyframes pulseGlow {
      0% { box-shadow: 0 0 12px rgba(255, 184, 0, 0.35); transform: scale(1); }
      100% { box-shadow: 0 0 24px rgba(255, 184, 0, 0.65); transform: scale(1.03); }
    }
"""

if '.coin-badge' not in content:
    content = content.replace('.action-text {', extra_css + '\n    .action-text {')

# 2. Update .action-icon-img size to 52px for 3D icons
content = re.sub(
    r'\.action-icon-img\s*\{[^}]*\}',
    """.action-icon-img {
      width: 52px;
      height: 52px;
      object-fit: contain;
      filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.55));
    }""",
    content
)

# 3. Update CMD banner (Strictly 2-3 free interactions, NO free laugh)
content = re.sub(
    r'<div class="cmd-banner">[\s\S]*?</div>\s*</div>',
    """<div class="cmd-banner">
      <div class="cmd-title">免费互动：发送 <span>666 蹦跳</span> / <span>888 吐泡泡</span> / <span>睡觉 呼呼</span></div>
      <div class="cmd-subtitle">发弹幕即刻互动 · 送「八级大笑」看奶娃变大抱肚狂笑！</div>
    </div>""",
    content
)

# 4. Update the left and right gift panels with 100% authentic Douyin icons & names
new_left_gifts = """    <!-- 3. 左侧动作指令列表 (抖音官方真实入门礼物 · 1~5抖币) -->
    <div class="action-side side-left">
      <div class="action-tag" onclick="triggerAction('blush')">
        <img class="action-icon-img" src="assets/gifts/xindong.png" alt="小心心">
        <span class="action-text">小心心 <span class="coin-badge">1抖币</span></span>
      </div>
      <div class="action-tag" onclick="triggerAction('boing')">
        <img class="action-icon-img" src="assets/gifts/douyin_note.png" alt="抖音">
        <span class="action-text">抖音 <span class="coin-badge">1抖币</span></span>
      </div>
      <div class="action-tag" onclick="triggerAction('rose')">
        <img class="action-icon-img" src="assets/gifts/meigui.png" alt="玫瑰">
        <span class="action-text">玫瑰 <span class="coin-badge">1抖币</span></span>
      </div>
      <div class="action-tag" onclick="triggerAction('praise')">
        <img class="action-icon-img" src="assets/gifts/renqipiao.png" alt="人气票">
        <span class="action-text">人气票 <span class="coin-badge">1抖币</span></span>
      </div>
      <div class="action-tag" onclick="triggerAction('hearts')">
        <img class="action-icon-img" src="assets/gifts/bixin.png" alt="手势比心">
        <span class="action-text">手势比心 <span class="coin-badge">5抖币</span></span>
      </div>
    </div>"""

new_right_gifts = """    <!-- 4. 右侧动作指令列表 (抖音官方真实互动礼物 · 9~99抖币) -->
    <div class="action-side side-right">
      <div class="action-tag" onclick="triggerAction('bubbles')">
        <span class="action-text">棒棒糖 <span class="coin-badge">9抖币</span></span>
        <img class="action-icon-img" src="assets/gifts/bangbangtang.png" alt="棒棒糖">
      </div>
      <div class="action-tag" onclick="triggerAction('bloat')">
        <span class="action-text">甜甜圈 <span class="coin-badge">10抖币</span></span>
        <img class="action-icon-img" src="assets/gifts/tiantianquan.png" alt="甜甜圈">
      </div>
      <div class="action-tag special-glow" onclick="triggerAction('belly_laugh')" title="【核心主推】触发变大抱肚子魔性狂笑">
        <span class="action-text" style="color: #ffd043; font-weight: 800;">八级大笑 <span class="coin-badge gold">19抖币</span></span>
        <img class="action-icon-img" src="assets/gifts/daxiao.png" alt="八级大笑">
      </div>
      <div class="action-tag" onclick="triggerAction('flower')">
        <span class="action-text">送你花花 <span class="coin-badge">49抖币</span></span>
        <img class="action-icon-img" src="assets/gifts/huahua.png" alt="送你花花">
      </div>
      <div class="action-tag" onclick="triggerAction('dance')">
        <span class="action-text">墨镜 <span class="coin-badge">99抖币</span></span>
        <img class="action-icon-img" src="assets/gifts/mojing.png" alt="墨镜">
      </div>
    </div>"""

content = re.sub(
    r'<!-- 3\. 左侧动作指令列表[\s\S]*?<!-- 4\. 右侧动作指令列表[\s\S]*?</div>\s*</div>',
    new_left_gifts + '\n\n' + new_right_gifts,
    content
)

# 5. Update director panel buttons
new_director_grid = """    <div class="btn-grid">
      <button class="ctrl-btn" onclick="triggerAction('blush')">💖 小心心 1抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('boing')">🎵 抖音 1抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('rose')">🌹 玫瑰 1抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('praise')">🎟️ 人气票 1抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('hearts')">🫰 手势比心 5抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('bubbles')">🍭 棒棒糖 9抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('bloat')">🍩 甜甜圈 10抖币</button>
      <button class="ctrl-btn special" onclick="triggerAction('belly_laugh')">🤣 八级大笑 19抖币 (抱肚大笑)</button>
      <button class="ctrl-btn" onclick="triggerAction('flower')">🌸 送你花花 49抖币</button>
      <button class="ctrl-btn special" onclick="triggerAction('dance')">🕶️ 墨镜 99抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('sleep')">😴 睡觉呼呼</button>
      <button class="ctrl-btn" onclick="testTalking()">🗣️ 说话嘴型</button>
      <button class="ctrl-btn" onclick="mockDanmaku()">💬 随机弹幕</button>
      <button class="ctrl-btn special" id="btn-play-toggle" onclick="toggleBgmPlay()">🎵 播/暂停BGM</button>
      <button class="ctrl-btn" onclick="skipSong()">⏭️ 下一首</button>
    </div>"""

content = re.sub(
    r'<div class="btn-grid">[\s\S]*?</div>',
    new_director_grid,
    content
)

# 6. Update actions to match gifts precisely
content = content.replace("showGiftToast('甜心宝贝', '小心心', 0.2, '💖');", "showGiftToast('甜心宝贝', '小心心', 0.2, '💖');")
content = content.replace("showGiftToast('铁杆粉', '粉丝灯牌', 0.2, '💡');", "showGiftToast('音符达人', '抖音', 0.2, '🎵');")
content = content.replace("showGiftToast('爽朗大哥', '大啤酒', 0.4, '🍺');", "showGiftToast('甜食控', '甜甜圈', 1.0, '🍩');")
content = content.replace("showGiftToast('热心老铁', '加油鸭 (八级大笑)', 3.0, '🦆');", "showGiftToast('超级老铁', '八级大笑', 3.8, '🤣');")
content = content.replace("showGiftToast('爱意满满', '鲜花', 2.0, '💐');", "showGiftToast('浪漫至死', '送你花花', 4.9, '🌸');")
content = content.replace("showGiftToast('潮流酷盖', '帅气墨镜', 3.8, '🕶️');", "showGiftToast('潮流酷盖', '墨镜', 9.9, '🕶️');")

# 7. Update danmaku handler: free commands only for boing, bubbles, sleep;
# Paid commands like laugh guide user to send gifts!
new_danmaku_func = """    // 智能解析弹幕口令 (严格规范商业化：基础动作免费，大招专属引导送礼)
    function handleDanmakuCommand(user, text) {
      addDanmaku(user, text);
      const t = text.trim();
      
      // 1. 免费互动指令 (基础轻量互动)
      if (t.includes('666') || t.includes('蹦') || t.includes('跳')) {
        triggerAction('boing');
      } else if (t.includes('888') || t.includes('泡泡')) {
        triggerAction('bubbles');
      } else if (t.includes('睡') || t.includes('呼呼')) {
        triggerAction('sleep');
      } 
      // 2. 商业化引导：弹幕发送付费特技关键词，语音智能提醒送礼
      else if (t.includes('大笑') || t.includes('八级') || t.includes('笑') || t.includes('肚子')) {
        startTalking('大笑肚皮会抽筋的～送出右侧【八级大笑】才能看到奶娃变大抱肚狂笑哦～');
      } else if (t.includes('墨镜') || t.includes('跳舞')) {
        startTalking('戴上墨镜才会跳舞哦～送出右侧【墨镜】看奶娃酷炫街舞～');
      } else {
        startTalking(text);
        setTimeout(stopTalking, 3500);
      }
    }"""

content = re.sub(
    r'// 智能解析弹幕口令[\s\S]*?function handleDanmakuCommand[\s\S]*?setTimeout\(stopTalking, 3500\);\s*\}\s*\}',
    new_danmaku_func.strip(),
    content
)

with open('douyin_live/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated douyin_live/index.html with authentic 3D gift icons and product hierarchy!")
