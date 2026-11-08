# -*- coding: utf-8 -*-
with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. 确保 window.pendingVipUsers 在 script 顶部声明
top_marker = "const viewport = document.getElementById('viewport-container');"
c = c.replace(top_marker, "window.pendingVipUsers = {};\n    " + top_marker)

# 2. 移除后面低处的 const pendingVipUsers = {};
c = c.replace("const pendingVipUsers = {}; // { '用户名': timestamp }", "// pendingVipUsers 已提升至顶部全局")
c = c.replace("const pendingVipUsers = {};", "")

# 3. 增强 extractSongName 函数
old_extract_func = """    // 智能从文本中提取观众想点的歌名
    function extractSongName(text) {
      let cleaned = text.trim();
      cleaned = cleaned.replace(/[\\[\\]]/g, '').trim();
      
      const keywords = ['点歌', '想听', '播放', '来一首', '唱一首', '听', '插队', '指定'];
      for (let kw of keywords) {
        if (cleaned.includes(kw)) {
          const idx = cleaned.indexOf(kw);
          const song = cleaned.substring(idx + kw.length).replace(/[:：]/g, '').trim();
          if (song) return song.replace(/[《》]/g, '');
        }
      }

      // 如果包含礼物名，剔除礼物名后剩下的作为歌名
      for (let g in GIFT_ACTION_MAP) {
        cleaned = cleaned.replace(g, '').trim();
      }
      cleaned = cleaned.replace(/^(送出|送了|来个|插队|VIP点歌|指定点歌|x\\d+)/, '').trim();
      if (cleaned.length >= 2 && cleaned.length <= 16) {
        return cleaned.replace(/[《》]/g, '');
      }
      return null;
    }"""

new_extract_func = """    // 智能从文本中提取观众想点的歌名
    function extractSongName(text) {
      if (!text) return null;
      let cleaned = text.trim().replace(/[\\[\\]《》]/g, '').trim();
      
      // 1. 优先匹配显式点歌关键词
      const keywords = ['点歌', '想听', '播放', '来一首', '唱一首', '听', '插队', '指定'];
      for (let kw of keywords) {
        if (cleaned.includes(kw)) {
          const idx = cleaned.indexOf(kw);
          const song = cleaned.substring(idx + kw.length).replace(/[:：]/g, '').trim();
          if (song && song.length >= 2) return song;
        }
      }

      // 2. 如果包含送礼文本，剔除送礼部分
      let stripped = cleaned;
      for (let g in GIFT_ACTION_MAP) {
        stripped = stripped.replace(g, '').trim();
      }
      stripped = stripped.replace(/^(送出|送了|来个|插队|VIP点歌|指定点歌|x\\d+|\\*\\d+|[0-9]+个)+/g, '').trim();
      
      // 如果剔除送礼前缀后剩下的文字是具体歌名 (2~15字且不是纯数字/代号)
      if (stripped.length >= 2 && stripped.length <= 16 && !/^[0-9xX*\\s]+$/.test(stripped)) {
        return stripped;
      }
      return null;
    }"""

c = c.replace(old_extract_func, new_extract_func)

# 4. 优化 handleGiftEvent 与 handleDanmakuCommand
old_gift_event_caller = """      // A. 自动检测送礼字符串 (例如 "[送出 棒棒糖 x1]"、"送出 棒棒糖"、"送出 为你点亮")
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
      }"""

new_gift_event_caller = """      // A. 自动检测送礼字符串 (例如 "[送出 棒棒糖 x1]"、"送出 为你点亮 点歌 孤勇者")
      if (t.includes('送出') || t.includes('送了') || t.startsWith('[')) {
        for (let g in GIFT_ACTION_MAP) {
          if (t.includes(g)) {
            const numMatch = t.match(/[xX*×](\\d+)/);
            const count = numMatch ? parseInt(numMatch[1]) : 1;
            addDanmaku(user, t, true);
            handleGiftEvent(user, g, count, t);
            return;
          }
        }
      }"""

c = c.replace(old_gift_event_caller, new_gift_event_caller)

# 5. 更新 handleGiftEvent 签名支持 rawText
old_gift_sig = "function handleGiftEvent(user, giftName, count = 1) {"
new_gift_sig = "function handleGiftEvent(user, giftName, count = 1, rawText = '') {"
c = c.replace(old_gift_sig, new_gift_sig)

# 6. 更新 handleGiftEvent 中的 vip_song 处理
old_vip_song_block = """        if (match.action === 'vip_song') {
          // 为你点亮送出：将该用户登记到 VIP 挂起池 (90秒内打字自动识别为指定歌名)
          pendingVipUsers[user] = Date.now();
          // 如果当前礼物附带了歌名则直接使用，否则随机挑选热门歌曲先行插队并语音引导指定
          const specifiedSong = extractSongName(user + ' ' + giftName);
          const finalSong = specifiedSong || TRENDING_HOT_SONGS[Math.floor(Math.random() * TRENDING_HOT_SONGS.length)].title;
          handleSongRequest(finalSong, user, true);
        }"""

new_vip_song_block = """        if (match.action === 'vip_song') {
          // 为你点亮送出：登记该用户到 VIP 挂起池 (90秒内发任何文字直接识别为指定歌名)
          window.pendingVipUsers[user] = Date.now();
          // 如果弹幕同一句已经带了歌名 (例如: "[送出 为你点亮 x1] 点歌 孤勇者")
          const specifiedSong = extractSongName(rawText);
          if (specifiedSong) {
            delete window.pendingVipUsers[user];
            handleSongRequest(specifiedSong, user, true);
          } else {
            // 观众先送礼、后发歌名：默认先送上一首热门主打歌，奶娃亲口引导小主人发歌名
            const defaultSong = "爱如火 (极乐净土版)";
            handleSongRequest(defaultSong, user, true);
            playNaiwaAudio(ACTION_VOICES.song, `哇！感谢【${user}】送出【为你点亮】！小主人想听什么歌？快在公屏发送歌名，奶娃立刻为你插队换歌哦～`, true);
          }
        }"""

c = c.replace(old_vip_song_block, new_vip_song_block)

# 7. 更新 handleDanmakuCommand 中的 pendingVipUsers 消费逻辑
old_consume_block = """      // B. 智能识别：检查该观众是否刚送过【为你点亮】(处于 90 秒 VIP 优先指定窗口)
      if (pendingVipUsers[user] && (Date.now() - pendingVipUsers[user] < 90000)) {
        const extracted = extractSongName(t) || t.replace(/[《》]/g, '').trim();
        delete pendingVipUsers[user]; // 消费掉 VIP 特权
        playNaiwaAudio(ACTION_VOICES.song, `收到【${user}】的VIP指定歌单！已立即插队为你切换到《${extracted}》！`, true);
        handleSongRequest(extracted, user, true);
        return;
      }"""

new_consume_block = """      // B. 智能识别：检查该观众是否刚送过【为你点亮】(处于 90 秒 VIP 优先指定窗口)
      if (window.pendingVipUsers && window.pendingVipUsers[user] && (Date.now() - window.pendingVipUsers[user] < 90000)) {
        const extracted = extractSongName(t) || t.replace(/[《》]/g, '').trim();
        delete window.pendingVipUsers[user]; // 成功消费掉 VIP 特权
        playNaiwaAudio(ACTION_VOICES.song, `收到【${user}】的VIP指定歌单！已立即插队为你切换到《${extracted}》！`, true);
        handleSongRequest(extracted, user, true);
        return;
      }"""

c = c.replace(old_consume_block, new_consume_block)

with open('douyin_live/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed TDZ and perfected VIP song association flow!")
