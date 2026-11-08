# -*- coding: utf-8 -*-
with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. 在 WebSocket 消息处理中增加对 type === 'gift' 和 type === 'song_request' 的结构化解析
old_ws_msg = """            if (data.type === 'llm_delta' || data.text) {
              const txt = data.text || data.delta;
              startTalking(txt);
            }

            if (data.type === 'audio_end' || data.status === 'finish') {
              stopTalking();
            }

            if (data.danmaku) {
              handleDanmakuCommand(data.user, data.danmaku);
            }"""

new_ws_msg = """            if (data.type === 'llm_delta' || data.text) {
              const txt = data.text || data.delta;
              startTalking(txt);
            }

            if (data.type === 'audio_end' || data.status === 'finish') {
              stopTalking();
            }

            // 1. 结构化礼物事件直连 (接收来自抓取器/后端的送礼事件)
            if (data.type === 'gift' || data.gift) {
              handleGiftEvent(data.user || '热心观众', data.gift, data.count || 1);
            }
            // 2. 结构化点歌事件直连
            else if (data.type === 'song_request' || data.song) {
              handleSongRequest(data.song, data.user || '热心观众', data.isPriority || false);
            }
            // 3. 弹幕消息事件
            else if (data.danmaku) {
              handleDanmakuCommand(data.user || '热心观众', data.danmaku);
            }"""

c = c.replace(old_ws_msg, new_ws_msg)

# 2. 增加全局 GIFT_ACTION_MAP 与 handleGiftEvent 核心引擎，并升级 handleDanmakuCommand
old_danmaku_section = """    // 智能解析弹幕口令 (严格规范商业化：直接发中文词触发动作，大招专属引导送礼)
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

new_danmaku_section = """    // =======================================================
    // 抖音官方礼物核心分发引擎 (礼物事件 ➔ 动作特技 ➔ 跑道横幅 ➔ 喂饭进度)
    // =======================================================
    const GIFT_ACTION_MAP = {
      '小心心': { action: 'blush', bowls: 0.2, icon: '💖' },
      '心动': { action: 'blush', bowls: 0.2, icon: '💖' },
      '抖音': { action: 'boing', bowls: 0.2, icon: '🎵' },
      '玫瑰': { action: 'rose', bowls: 0.2, icon: '🌹' },
      '人气票': { action: 'praise', bowls: 0.2, icon: '🎟️' },
      '大啤酒': { action: 'pijiu', bowls: 0.4, icon: '🍺' },
      '啤酒': { action: 'pijiu', bowls: 0.4, icon: '🍺' },
      '你最好看': { action: 'haokan', bowls: 0.4, icon: '✨' },
      '好看': { action: 'haokan', bowls: 0.4, icon: '✨' },
      '手势比心': { action: 'hearts', bowls: 1.0, icon: '🫰' },
      '比心': { action: 'hearts', bowls: 1.0, icon: '🫰' },
      '为你点亮': { action: 'vip_song', bowls: 1.8, icon: '⭐' },
      '点亮': { action: 'vip_song', bowls: 1.8, icon: '⭐' },
      '甜甜圈': { action: 'donut', bowls: 2.0, icon: '🍩' },
      '棒棒糖': { action: 'belly_laugh', bowls: 1.8, icon: '🍭' }
    };

    function handleGiftEvent(user, giftName, count = 1) {
      if (!giftName) return;
      const cleanGift = giftName.replace(/[\\[\\]送出xX0-9]/g, '').trim();
      
      // 查找映射表
      let match = null;
      for (let k in GIFT_ACTION_MAP) {
        if (cleanGift.includes(k) || k.includes(cleanGift)) {
          match = GIFT_ACTION_MAP[k];
          break;
        }
      }

      const icon = match ? match.icon : '🎁';
      const bowls = match ? match.bowls * count : 0.2 * count;
      
      // 1. 跑道飘窗展示专属特效横幅
      showGiftToast(user, `${cleanGift} x${count}`, bowls, icon);

      // 2. 增加白饭与更新心愿进度条
      feedRice(bowls);

      // 3. 触发专属特技与动效
      if (match) {
        triggerAction(match.action);
      } else {
        triggerAction('blush'); // 默认未知礼物害羞感谢
      }
    }

    // 智能解析弹幕口令 (支持送礼文本抓取解析、免费中文词触发动作、大招专属引导送礼)
    function handleDanmakuCommand(user, text) {
      const t = text.trim();

      // A. 自动检测送礼字符串 (例如 "[送出 棒棒糖 x1]"、"送出 棒棒糖"、"送出 为你点亮")
      if (t.includes('送出') || t.includes('送了') || t.startsWith('[')) {
        for (let g in GIFT_ACTION_MAP) {
          if (t.includes(g)) {
            const numMatch = t.match(/[xX*×](\\d+)/);
            const count = numMatch ? parseInt(numMatch[1]) : 1;
            addDanmaku(user, t, true);
            handleGiftEvent(user, g, count);
            return;
          }
        }
      }

      // 普通弹幕列表追加
      addDanmaku(user, text, false);

      // B. 点歌与VIP插队点歌检测
      if (t.includes('插队') || t.includes('为你点亮')) {
        handleSongRequest(t, user, true);
        return;
      }
      if (t.startsWith('点歌') || t.startsWith('播放') || t.startsWith('想听')) {
        handleSongRequest(t, user, false);
        return;
      }

      // C. 免费互动指令 (中文动作词直接触发)
      if (t.includes('蹦跳') || t.includes('跳') || t.includes('666')) {
        triggerAction('boing');
      } else if (t.includes('吐泡泡') || t.includes('泡泡') || t.includes('888')) {
        triggerAction('bubbles');
      } else if (t.includes('睡觉') || t.includes('呼呼') || t.includes('睡')) {
        triggerAction('sleep');
      } 
      // D. 商业化引导：公屏白嫖发大笑，语音智能提醒送礼
      else if (t.includes('大笑') || t.includes('抱肚子') || t.includes('笑') || t.includes('狂笑')) {
        startTalking('大笑肚皮会抽筋的～送一个右侧【棒棒糖】就能看奶娃变大抱肚狂笑啦～');
      } else if (t.includes('啤酒') || t.includes('喝')) {
        startTalking('想看奶娃吨吨吨吗？送一个【大啤酒】看奶娃打饱嗝哦～');
      } else if (t.includes('点亮') || t.includes('飞')) {
        startTalking('送一个【为你点亮】看奶娃VIP插队点歌与唯美升空哦～');
      } else {
        startTalking(text);
        setTimeout(stopTalking, 3500);
      }
    }"""

c = c.replace(old_danmaku_section, new_danmaku_section)

# 3. 将 handleGiftEvent 挂载到 window，确保外部脚本/抓取器可直接调用
c = c.replace("window.feedRice = feedRice;", "window.feedRice = feedRice;\n    window.handleGiftEvent = handleGiftEvent;\n    window.handleDanmakuCommand = handleDanmakuCommand;")

with open('douyin_live/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Added handleGiftEvent & robust gift dispatcher to index.html!")
