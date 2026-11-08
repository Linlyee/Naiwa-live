# -*- coding: utf-8 -*-
import re

html_path = 'douyin_live/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修复 pulseGlow 语法残留
old_glow = """    @keyframes pulseGlow {
      0% { box-shadow: 0 0 10px rgba(255, 184, 0, 0.35); }
      100% { box-shadow: 0 0 22px rgba(255, 184, 0, 0.7); }
    }
      100% { box-shadow: 0 0 24px rgba(255, 184, 0, 0.65); transform: scale(1.03); }
    }"""
new_glow = """    @keyframes pulseGlow {
      0% { box-shadow: 0 0 10px rgba(255, 184, 0, 0.35); }
      100% { box-shadow: 0 0 22px rgba(255, 184, 0, 0.7); }
    }"""
content = content.replace(old_glow, new_glow)

# 2. 顶部免费口令条：去 666/888，采用纯中文动作词
old_banner = """    <!-- 2. 免费互动口令条 -->
    <div class="cmd-banner">
      <div class="cmd-title">免费互动：发送 <span>666 蹦跳</span> / <span>888 吐泡泡</span> / <span>睡觉 呼呼</span></div>
      <div class="cmd-subtitle">发弹幕即刻互动 · 送「八级大笑」看奶娃变大抱肚狂笑！</div>
    </div>"""

new_banner = """    <!-- 2. 免费互动口令条 -->
    <div class="cmd-banner">
      <div class="cmd-title">免费互动：发送 <span>「蹦跳」</span> / <span>「吐泡泡」</span> / <span>「睡觉」</span></div>
      <div class="cmd-subtitle">发弹幕即刻互动 · 送「棒棒糖」看奶娃变大抱肚狂笑！</div>
    </div>"""
content = content.replace(old_banner, new_banner)

# 3. 左右两侧动作指令列表：全部换成抖音官方 1~10 抖币真实礼物，棒棒糖对应抱肚子狂笑
old_sides = """            <!-- 3. 左侧动作指令列表 (抖音官方真实入门礼物 · 1~5抖币) -->
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
    </div>

    <!-- 4. 右侧动作指令列表 (抖音官方真实互动礼物 · 9~99抖币) -->
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

new_sides = """            <!-- 3. 左侧动作指令列表 (抖音官方真实入门礼物 · 1~2抖币) -->
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
      <div class="action-tag" onclick="triggerAction('pijiu')">
        <img class="action-icon-img" src="assets/gifts/pijiu.png" alt="大啤酒">
        <span class="action-text">大啤酒 <span class="coin-badge">2抖币</span></span>
      </div>
    </div>

    <!-- 4. 右侧动作指令列表 (抖音官方真实热门礼物 · 2~10抖币) -->
    <div class="action-side side-right">
      <div class="action-tag" onclick="triggerAction('haokan')">
        <span class="action-text">你最好看 <span class="coin-badge">2抖币</span></span>
        <img class="action-icon-img" src="assets/gifts/haokan.png" alt="你最好看">
      </div>
      <div class="action-tag" onclick="triggerAction('hearts')">
        <span class="action-text">手势比心 <span class="coin-badge">5抖币</span></span>
        <img class="action-icon-img" src="assets/gifts/bixin.png" alt="手势比心">
      </div>
      <div class="action-tag" onclick="triggerAction('balloon')">
        <span class="action-text">为你点亮 <span class="coin-badge">9抖币</span></span>
        <img class="action-icon-img" src="assets/gifts/zhaixing.png" alt="为你点亮">
      </div>
      <div class="action-tag" onclick="triggerAction('donut')">
        <span class="action-text">甜甜圈 <span class="coin-badge">10抖币</span></span>
        <img class="action-icon-img" src="assets/gifts/tiantianquan.png" alt="甜甜圈">
      </div>
      <div class="action-tag special-glow" onclick="triggerAction('belly_laugh')" title="【核心王牌特技】送棒棒糖看奶娃变大抱肚狂笑">
        <span class="action-text" style="color: #ffd043; font-weight: 800;">棒棒糖 <span class="coin-badge gold">9抖币·狂笑</span></span>
        <img class="action-icon-img" src="assets/gifts/bangbangtang.png" alt="棒棒糖">
      </div>
    </div>"""
content = content.replace(old_sides, new_sides)

# 4. 底部弹幕初始列表
old_danmaku_init = """      <div class="danmaku-list" id="danmaku-list">
        <div class="danmaku-msg"><span class="user-name">陆泽:</span> 888</div>
        <div class="danmaku-msg"><span class="user-name">uchiha.:</span> 你今年几岁啦？</div>
        <div class="danmaku-msg"><span class="user-name">GGboy:</span> <span class="gift-badge">[送出 棒棒糖 x1]</span></div>
      </div>"""

new_danmaku_init = """      <div class="danmaku-list" id="danmaku-list">
        <div class="danmaku-msg"><span class="user-name">陆泽:</span> 蹦跳</div>
        <div class="danmaku-msg"><span class="user-name">uchiha.:</span> 你今年几岁啦？</div>
        <div class="danmaku-msg"><span class="user-name">GGboy:</span> <span class="gift-badge">[送出 棒棒糖 x1]</span></div>
      </div>"""
content = content.replace(old_danmaku_init, new_danmaku_init)

# 5. 导演台按钮
old_ctrl_btn = """        <div class="btn-grid">
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

new_ctrl_btn = """        <div class="btn-grid">
      <button class="ctrl-btn" onclick="triggerAction('blush')">💖 小心心 1抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('boing')">🎵 抖音 1抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('rose')">🌹 玫瑰 1抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('praise')">🎟️ 人气票 1抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('pijiu')">🍺 大啤酒 2抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('haokan')">✨ 你最好看 2抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('hearts')">🫰 手势比心 5抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('balloon')">⭐ 为你点亮 9抖币</button>
      <button class="ctrl-btn" onclick="triggerAction('donut')">🍩 甜甜圈 10抖币</button>
      <button class="ctrl-btn special" onclick="triggerAction('belly_laugh')">🍭 棒棒糖 9抖币 (抱肚狂笑)</button>
      <button class="ctrl-btn" onclick="triggerAction('boing')">🦘 弹幕「蹦跳」</button>
      <button class="ctrl-btn" onclick="triggerAction('bubbles')">🫧 弹幕「吐泡泡」</button>
      <button class="ctrl-btn" onclick="triggerAction('sleep')">😴 弹幕「睡觉」</button>
      <button class="ctrl-btn" onclick="testTalking()">🗣️ 说话嘴型</button>
      <button class="ctrl-btn" onclick="mockDanmaku()">💬 随机弹幕</button>
      <button class="ctrl-btn special" id="btn-play-toggle" onclick="toggleBgmPlay()">🎵 播/暂停BGM</button>
      <button class="ctrl-btn" onclick="skipSong()">⏭️ 下一首</button>
    </div>"""
content = content.replace(old_ctrl_btn, new_ctrl_btn)

# 6. JS triggerAction 中的各个 action 逻辑
# 检查原 belly_laugh 结束文案
content = content.replace("谢谢哥哥姐姐的八级大笑！", "谢谢哥哥姐姐送的棒棒糖！")
content = content.replace("showGiftToast('超级老铁', '八级大笑', 3.8, '🤣');", "showGiftToast('超级老铁', '棒棒糖', 1.8, '🍭');")

# 7. 添加 pijiu 和 haokan action
action_hook = """        case 'praise': // 人气票 (1抖币 · 抖音官方热门礼物)
          playNaiwaAudio(ACTION_VOICES.song, '哇！谢谢大家的人气票支持！奶娃超开心~', true);
          rig.className = 'character-rig anim-boing';
          setEyes('star');
          setMouth('open');
          spawnGPUParticles('🎟️', 25);
          spawnGPUParticles('✨', 20);
          feedRice(0.2);
          showGiftToast('忠实铁粉', '人气票', 0.2, '🎟️');
          currentActionTimeout = setTimeout(resetToIdle, 2200);
          break;"""

if "case 'pijiu':" not in content:
    # 查找 praise 的位置并替换/扩展
    praise_regex = r"(case 'praise':.*?\n\s+currentActionTimeout = setTimeout\(resetToIdle, \d+\);\s+break;)"
    match = re.search(praise_regex, content, re.DOTALL)
    if match:
        orig_praise = match.group(1)
        extended_cases = orig_praise + """

        case 'pijiu': // 大啤酒 (2抖币 · 豪爽干杯)
          playNaiwaAudio(ACTION_VOICES.hungry, '吨吨吨……哈！好爽的大啤酒！嗝～', true);
          rig.className = 'character-rig anim-spicy';
          setEyes('dizzy');
          setMouth('o');
          spawnGPUParticles('🍺', 28);
          feedRice(0.4);
          showGiftToast('豪爽大哥', '大啤酒', 0.4, '🍺');
          currentActionTimeout = setTimeout(resetToIdle, 2400);
          break;

        case 'haokan': // 你最好看 (2抖币 · 抖音官方热门礼物)
          playNaiwaAudio(ACTION_VOICES.song, '哇！你才最好看呢！心里美滋滋的~', true);
          rig.className = 'character-rig anim-boing';
          setEyes('star');
          setMouth('open');
          layerBlush.style.opacity = '0.95';
          spawnGPUParticles('✨', 35);
          spawnGPUParticles('💖', 15);
          feedRice(0.4);
          showGiftToast('眼光真好', '你最好看', 0.4, '✨');
          currentActionTimeout = setTimeout(resetToIdle, 2400);
          break;"""
        content = content.replace(orig_praise, extended_cases)

# 8. 弹幕口令 handleDanmakuCommand
old_danmaku_func = """    // 智能解析弹幕口令 (严格规范商业化：基础动作免费，大招专属引导送礼)
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

new_danmaku_func = """    // 智能解析弹幕口令 (严格规范商业化：直接发中文词触发动作，大招专属引导送礼)
    function handleDanmakuCommand(user, text) {
      addDanmaku(user, text);
      const t = text.trim();
      
      // 1. 免费互动指令 (中文动作词直接触发)
      if (t.includes('蹦跳') || t.includes('跳') || t.includes('666')) {
        triggerAction('boing');
      } else if (t.includes('吐泡泡') || t.includes('泡泡') || t.includes('888')) {
        triggerAction('bubbles');
      } else if (t.includes('睡觉') || t.includes('呼呼') || t.includes('睡')) {
        triggerAction('sleep');
      } 
      // 2. 商业化引导：弹幕发送付费特技关键词，语音智能提醒送礼
      else if (t.includes('大笑') || t.includes('抱肚子') || t.includes('笑') || t.includes('狂笑')) {
        startTalking('大笑肚皮会抽筋的～送一个右侧【棒棒糖】就能看奶娃变大抱肚狂笑啦～');
      } else if (t.includes('啤酒') || t.includes('喝')) {
        startTalking('想看奶娃吨吨吨吗？送一个【大啤酒】看奶娃打饱嗝哦～');
      } else if (t.includes('点亮') || t.includes('飞')) {
        startTalking('送一个【为你点亮】看奶娃唯美升空漫游哦～');
      } else {
        startTalking(text);
        setTimeout(stopTalking, 3500);
      }
    }"""
content = content.replace(old_danmaku_func, new_danmaku_func)

# 9. mockDanmaku 中的示例
old_mock = """      const samples = [
        { u: '追光者', t: '666', cmd: 'boing' },
        { u: '甜心布丁', t: '[送出 小心心 x1]', isGift: true, cmd: 'blush' },
        { u: '大西瓜', t: '888', cmd: 'bubbles' },
        { u: '老六本六', t: '[送出 八级大笑 x1]', isGift: true, cmd: 'belly_laugh' },
        { u: '吃货小美', t: '[送出 甜甜圈 x1]', isGift: true, cmd: 'donut' },
        { u: '陆泽哥哥', t: '[送出 辣条 x1]', isGift: true, cmd: 'spicy' },
        { u: '可乐加冰', t: '[送出 快乐水 x1]', isGift: true, cmd: 'bloat' },
        { u: '夜猫子', t: '困了，快睡觉吧', cmd: 'sleep' },
        { u: '爱笑的草莓', t: '[送出 恶搞板砖 x1]', isGift: true, cmd: 'squish' },
        { u: '酷酷的阿强', t: '[送出 帅气墨镜 x1]', isGift: true, cmd: 'dance' },
        { u: '糖果派对', t: '[送出 彩虹气球 x1]', isGift: true, cmd: 'balloon' }
      ];"""

new_mock = """      const samples = [
        { u: '追光者', t: '蹦跳', cmd: 'boing' },
        { u: '甜心布丁', t: '[送出 小心心 x1]', isGift: true, cmd: 'blush' },
        { u: '大西瓜', t: '吐泡泡', cmd: 'bubbles' },
        { u: '老六本六', t: '[送出 棒棒糖 x1]', isGift: true, cmd: 'belly_laugh' },
        { u: '吃货小美', t: '[送出 甜甜圈 x1]', isGift: true, cmd: 'donut' },
        { u: '豪爽二哥', t: '[送出 大啤酒 x1]', isGift: true, cmd: 'pijiu' },
        { u: '星空漫步', t: '[送出 为你点亮 x1]', isGift: true, cmd: 'balloon' },
        { u: '夜猫子', t: '睡觉', cmd: 'sleep' },
        { u: '小可爱', t: '[送出 手势比心 x1]', isGift: true, cmd: 'hearts' },
        { u: '粉丝牌铁粉', t: '[送出 玫瑰 x1]', isGift: true, cmd: 'rose' },
        { u: '榜一大哥', t: '[送出 你最好看 x1]', isGift: true, cmd: 'haokan' }
      ];"""
content = content.replace(old_mock, new_mock)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html successfully!")
