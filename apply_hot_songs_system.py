# -*- coding: utf-8 -*-
with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. 增加热门歌单卡片与模态框的 CSS
style_marker = "/* 底部点歌台 */"
new_styles = """    /* 热门点歌单卡片 (位于右下角弹幕区旁，无缝填补空白) */
    .song-sheet-card {
      position: absolute;
      bottom: 195px;
      right: 50px;
      width: 380px;
      height: 255px;
      background: rgba(16, 28, 44, 0.85);
      border: 1px solid rgba(255, 208, 67, 0.4);
      backdrop-filter: blur(14px);
      border-radius: 20px;
      padding: 12px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.45);
      z-index: 20;
    }

    .song-sheet-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 19px;
      font-weight: 800;
      color: #ffd043;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 6px;
    }

    .sheet-badge {
      background: linear-gradient(135deg, #ff9800, #ff5722);
      color: #ffffff;
      font-size: 13px;
      padding: 1px 7px;
      border-radius: 10px;
      font-weight: 700;
    }

    .song-sheet-list {
      display: flex;
      flex-direction: column;
      gap: 5px;
      margin: 4px 0;
    }

    .song-quick-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(255, 255, 255, 0.06);
      border-radius: 8px;
      padding: 4px 10px;
      font-size: 16px;
      color: #e0f0ff;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.18s, transform 0.15s, color 0.18s;
    }

    .song-quick-item:hover {
      background: rgba(255, 208, 67, 0.25);
      transform: translateX(4px);
      color: #ffd043;
    }

    .song-hot-tag {
      font-size: 12px;
      color: #ff9800;
      font-weight: 700;
    }

    .song-sheet-footer {
      font-size: 15px;
      color: var(--accent-blue);
      text-align: right;
      cursor: pointer;
      font-weight: 700;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .song-sheet-footer:hover { color: var(--accent-yellow); }

    /* 完整歌单弹窗 */
    .song-modal {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(16px);
      z-index: 9999;
      display: none;
      align-items: center;
      justify-content: center;
    }
    .song-modal.active { display: flex; }

    .song-modal-content {
      width: 780px;
      max-height: 85vh;
      background: #112032;
      border: 1.5px solid rgba(255, 208, 67, 0.5);
      border-radius: 28px;
      padding: 26px 32px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 15px 50px rgba(0, 0, 0, 0.8);
      overflow: hidden;
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 26px;
      font-weight: 800;
      color: #ffd043;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-bottom: 14px;
      margin-bottom: 16px;
    }

    .modal-close {
      background: none;
      border: none;
      color: #fff;
      font-size: 26px;
      cursor: pointer;
      padding: 4px 10px;
      border-radius: 8px;
    }
    .modal-close:hover { background: rgba(255,255,255,0.15); }

    .modal-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      overflow-y: auto;
      padding-right: 6px;
    }

    .modal-song-card {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 10px 16px;
      transition: background 0.2s, border-color 0.2s;
    }
    .modal-song-card:hover {
      background: rgba(255, 208, 67, 0.12);
      border-color: rgba(255, 208, 67, 0.4);
    }
    .modal-song-title { font-size: 18px; font-weight: 700; color: #fff; }
    .modal-song-cat { font-size: 13px; color: var(--text-sub); }
    .btn-pick-song {
      background: linear-gradient(135deg, #38ef7d, #11998e);
      border: none;
      color: #fff;
      font-size: 14px;
      font-weight: 700;
      border-radius: 8px;
      padding: 5px 12px;
      cursor: pointer;
    }
    .btn-pick-song:hover { transform: scale(1.05); }

    /* 底部点歌台 */"""

c = c.replace(style_marker, new_styles)

# 2. 插入热门歌单卡片与模态框的 HTML (位于 danmaku-box 下方，music-bar 上方)
html_marker = "<!-- 8. 底部点歌台 -->"
new_html = """    <!-- 7.5 右侧热门点歌单展示卡 (解决“别人不知道要什么歌”的痛点) -->
    <div class="song-sheet-card">
      <div class="song-sheet-header">
        <span>📜 热门歌单推荐</span>
        <span class="sheet-badge">24首精选</span>
      </div>
      <div class="song-sheet-list">
        <div class="song-quick-item" onclick="quickRequestSong('狂暴奶龙摇')">
          <span>1.《狂暴奶龙摇》</span>
          <span class="song-hot-tag">🔥 极火</span>
        </div>
        <div class="song-quick-item" onclick="quickRequestSong('爱如火 (极乐净土版)')">
          <span>2.《爱如火》</span>
          <span class="song-hot-tag">🔥 必点</span>
        </div>
        <div class="song-quick-item" onclick="quickRequestSong('孤勇者')">
          <span>3.《孤勇者》</span>
          <span class="song-hot-tag">🔥 热门</span>
        </div>
        <div class="song-quick-item" onclick="quickRequestSong('乌梅子酱')">
          <span>4.《乌梅子酱》</span>
          <span class="song-hot-tag">✨ 甜美</span>
        </div>
        <div class="song-quick-item" onclick="quickRequestSong('离别开出花')">
          <span>5.《离别开出花》</span>
          <span class="song-hot-tag">🌸 治愈</span>
        </div>
      </div>
      <div class="song-sheet-footer">
        <span style="color: #ffd043; font-size: 13px;">发「点歌 歌名」即点</span>
        <span onclick="toggleSongModal()" style="text-decoration: underline;">查看全部 24 首 ➔</span>
      </div>
    </div>

    <!-- 完整热门歌单全景弹窗 (24首精选) -->
    <div id="song-modal" class="song-modal" onclick="if(event.target===this) toggleSongModal()">
      <div class="song-modal-content">
        <div class="modal-header">
          <span>📜 奶娃私房精选歌单 · 观众点歌台 (共24首)</span>
          <button class="modal-close" onclick="toggleSongModal()">✕</button>
        </div>
        <div class="modal-grid" id="modal-song-grid">
          <!-- 动态渲染 24 首热门歌曲 -->
        </div>
        <div style="margin-top: 15px; display: flex; justify-content: space-between; align-items: center; color: var(--text-sub); font-size: 15px;">
          <span>💡 提示：公屏发送「点歌 歌名」即可免费排队；送「为你点亮」立即VIP霸权插队！</span>
          <button class="btn-pick-song" style="background: rgba(255,255,255,0.15);" onclick="toggleSongModal()">关闭</button>
        </div>
      </div>
    </div>

    <!-- 8. 底部点歌台 -->"""

c = c.replace(html_marker, new_html)

# 3. 增加精选曲库池、智能歌名提取、VIP 缓存状态池、10 分钟自动轮播引擎
script_hook = "// 默认常驻伴奏曲库"
new_script_engine = """    // =======================================================
    // 24首精选热门曲库池 (全覆盖抖音热榜、洗脑神曲、流行经典)
    // =======================================================
    const TRENDING_HOT_SONGS = [
      { title: "狂暴奶龙摇", cat: "🔥 奶龙洗脑神曲" },
      { title: "爱如火 (极乐净土版)", cat: "🔥 抖音热榜必点" },
      { title: "孤勇者", cat: "🔥 燃爆全场" },
      { title: "乌梅子酱", cat: "✨ 甜美治愈" },
      { title: "离别开出花", cat: "🌸 治愈流行" },
      { title: "勇气大爆发", cat: "🍼 萌娃神曲" },
      { title: "奢香夫人 (DJ版)", cat: "💃 动感摇摆" },
      { title: "大香蕉", cat: "🍌 欢乐鬼畜" },
      { title: "月声尽，心灯明", cat: "🏮 国风唯美" },
      { title: "演员", cat: "🎤 经典情歌" },
      { title: "晴天", cat: "☀️ 青春回忆" },
      { title: "恐龙抗狼", cat: "🦖 魔性节奏" },
      { title: "小苹果", cat: "🍎 国民神曲" },
      { title: "起风了", cat: "🍃 动听天籁" },
      { title: "稻香", cat: "🌾 温暖民谣" },
      { title: "少年", cat: "🏃 热血励志" },
      { title: "踏山河", cat: "⚔️ 豪迈古风" },
      { title: "白月光与朱砂痣", cat: "🌙 伤感情歌" },
      { title: "画绢", cat: "🎨 唯美国风" },
      { title: "下潜", cat: "🌊 氛围律动" },
      { title: "爱丫爱丫", cat: "💖 甜妹回忆" },
      { title: "芒种", cat: "🌾 热门国潮" },
      { title: "青花瓷", cat: "🏺 中国风代表" },
      { title: "极乐净土", cat: "🕺 宅舞鼻祖" }
    ];

    // 初始化渲染 24 首完整歌单
    function initSongGrid() {
      const grid = document.getElementById('modal-song-grid');
      if (!grid) return;
      grid.innerHTML = '';
      TRENDING_HOT_SONGS.forEach((song, idx) => {
        const item = document.createElement('div');
        item.className = 'modal-song-card';
        item.innerHTML = `
          <div>
            <div class="modal-song-title">${idx + 1}. 《${song.title}》</div>
            <div class="modal-song-cat">${song.cat}</div>
          </div>
          <button class="btn-pick-song" onclick="quickRequestSong('${song.title}')">点这首</button>
        `;
        grid.appendChild(item);
      });
    }

    function toggleSongModal() {
      const modal = document.getElementById('song-modal');
      if (modal) modal.classList.toggle('active');
    }

    // 快捷一键点歌
    function quickRequestSong(title) {
      toggleSongModal();
      handleSongRequest(title, '热心观众', false);
    }

    // =======================================================
    // 智能识别送礼人指定歌名机制 (解决“怎么识别送礼人点了什么歌”)
    // =======================================================
    // 挂起的 VIP 送礼用户池 (送了【为你点亮】后 90 秒内有效)
    const pendingVipUsers = {}; // { '用户名': timestamp }

    // 智能从文本中提取观众想点的歌名
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
    }

    // =======================================================
    // 10 分钟无观众点歌时，自动随机选一首当下热门歌曲
    // =======================================================
    let lastUserSongTime = Date.now();
    const IDLE_TIMEOUT_MS = 10 * 60 * 1000; // 10 分钟 (600,000 毫秒)
    let idleAutoDjTimer = null;

    function resetIdleTimer() {
      lastUserSongTime = Date.now();
    }

    // 启动 10 分钟自动轮播检查器
    function startIdleAutoDj() {
      if (idleAutoDjTimer) clearInterval(idleAutoDjTimer);
      idleAutoDjTimer = setInterval(() => {
        // 当排队列表为空时检查
        if (requestQueue.length === 0) {
          const idleElapsed = Date.now() - lastUserSongTime;
          if (idleElapsed >= IDLE_TIMEOUT_MS) {
            triggerAutoTrendingSong();
          }
        }
      }, 15000); // 每 15 秒轻量检测一次
    }

    // 触发自动热门歌曲播放
    function triggerAutoTrendingSong() {
      lastUserSongTime = Date.now();
      const pick = TRENDING_HOT_SONGS[Math.floor(Math.random() * TRENDING_HOT_SONGS.length)];
      
      const trackSrc = Math.random() > 0.5 ? "music/happy_chibi_bgm.mp3" : "music/sweet_lullaby_bgm.mp3";
      currentTrack = {
        title: pick.title,
        artist: "🔥 热门推荐 · 自动轮播",
        src: trackSrc,
        user: "系统推荐",
        isAutoTrending: true
      };

      bgmPlayer.src = currentTrack.src;
      bgmPlayer.play().then(() => {
        isPlaying = true;
        updateMusicUI();
        playNaiwaAudio(ACTION_VOICES.song, `现在直播间空闲啦，奶娃为大家随机挑选了当下热门金曲《${pick.title}》！发「点歌 歌名」可随时插播你想听的歌哦～`);
        addDanmaku("系统", `[🔥 10分钟空闲自动轮播热门歌曲 《${pick.title}》]`, false);
      }).catch(e => {
        updateMusicUI();
      });
    }

    // 默认常驻伴奏曲库"""

c = c.replace(script_hook, new_script_engine)

# 4. 更新 handleSongRequest 以更新 lastUserSongTime，并支持智能歌名识别与 VIP 缓存
old_song_request_impl = """    // 观众点歌核心处理函数 (全面支持免费弹幕排队与【为你点亮】9抖币 VIP 极速插队)
    function handleSongRequest(songName, userName = "热心观众", isPriority = false) {"""

new_song_request_impl = """    // 观众点歌核心处理函数 (全面支持免费弹幕排队与【为你点亮】9抖币 VIP 极速插队)
    function handleSongRequest(songName, userName = "热心观众", isPriority = false) {
      resetIdleTimer(); // 刷新 10 分钟空闲计时器"""

c = c.replace(old_song_request_impl, new_song_request_impl)

# 5. 更新 handleGiftEvent 中送出【为你点亮】时的智能指定识别与挂起
old_gift_handle_logic = """      // 3. 触发专属特技与动效
      if (match) {
        triggerAction(match.action);
      } else {
        triggerAction('blush'); // 默认未知礼物害羞感谢
      }"""

new_gift_handle_logic = """      // 3. 触发专属特技与动效
      if (match) {
        if (match.action === 'vip_song') {
          // 为你点亮送出：将该用户登记到 VIP 挂起池 (90秒内打字自动识别为指定歌名)
          pendingVipUsers[user] = Date.now();
          // 如果当前礼物附带了歌名则直接使用，否则随机挑选热门歌曲先行插队并语音引导指定
          const specifiedSong = extractSongName(user + ' ' + giftName);
          const finalSong = specifiedSong || TRENDING_HOT_SONGS[Math.floor(Math.random() * TRENDING_HOT_SONGS.length)].title;
          handleSongRequest(finalSong, user, true);
        } else {
          triggerAction(match.action);
        }
      } else {
        triggerAction('blush'); // 默认未知礼物害羞感谢
      }"""

c = c.replace(old_gift_handle_logic, new_gift_handle_logic)

# 6. 更新 handleDanmakuCommand 检查 pendingVipUsers
old_danmaku_command_song = """      // B. 点歌与VIP插队点歌检测
      if (t.includes('插队') || t.includes('为你点亮')) {
        handleSongRequest(t, user, true);
        return;
      }
      if (t.startsWith('点歌') || t.startsWith('播放') || t.startsWith('想听')) {
        handleSongRequest(t, user, false);
        return;
      }"""

new_danmaku_command_song = """      // B. 智能识别：检查该观众是否刚送过【为你点亮】(处于 90 秒 VIP 优先指定窗口)
      if (pendingVipUsers[user] && (Date.now() - pendingVipUsers[user] < 90000)) {
        const extracted = extractSongName(t) || t.replace(/[《》]/g, '').trim();
        delete pendingVipUsers[user]; // 消费掉 VIP 特权
        playNaiwaAudio(ACTION_VOICES.song, `收到【${user}】的VIP指定歌单！已立即插队为你切换到《${extracted}》！`, true);
        handleSongRequest(extracted, user, true);
        return;
      }

      // C. 弹幕中显式点歌与VIP插队点歌检测
      if (t.includes('插队') || t.includes('为你点亮')) {
        const songName = extractSongName(t) || t;
        handleSongRequest(songName, user, true);
        return;
      }
      if (t.startsWith('点歌') || t.startsWith('播放') || t.startsWith('想听') || t.startsWith('唱一首')) {
        const songName = extractSongName(t) || t;
        handleSongRequest(songName, user, false);
        return;
      }"""

c = c.replace(old_danmaku_command_song, new_danmaku_command_song)

# 7. 页面加载完成后启动自动歌单渲染与 10 分钟自动 DJ 定时器
old_init_timeout = """    // 页面加载后自动开启第一首伴奏
    setTimeout(() => {
      playNext();
    }, 800);"""

new_init_timeout = """    // 页面加载后自动初始化热门歌单与 10 分钟空闲自动 DJ 轮播
    setTimeout(() => {
      initSongGrid();
      startIdleAutoDj();
      playNext();
    }, 800);"""

c = c.replace(old_init_timeout, new_init_timeout)

with open('douyin_live/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Applied 3 major upgrades: Song Sheet UI, VIP Song Association, and 10-min Auto DJ!")
