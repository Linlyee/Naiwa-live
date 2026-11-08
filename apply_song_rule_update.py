# -*- coding: utf-8 -*-
with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. 移除右下角推荐歌单卡片与弹窗的 CSS，并重构 music-bar 与 music-tip CSS
old_style_block_start = "/* 热门点歌单卡片"
old_style_block_end = "/* 导演调试控制台 */"

start_idx = c.find(old_style_block_start)
end_idx = c.find(old_style_block_end)

if start_idx != -1 and end_idx != -1:
    new_music_style = """/* 底部点歌台 */
    .music-bar {
      position: absolute;
      bottom: 60px;
      left: 50px;
      right: 50px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      backdrop-filter: blur(12px);
      border-radius: 24px;
      padding: 16px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 20;
    }

    .music-info { display: flex; align-items: center; gap: 16px; flex: 1; min-width: 0; }
    .music-disc {
      width: 54px;
      height: 54px;
      border-radius: 50%;
      background: radial-gradient(circle, #2a3b4c 30%, #16222f 70%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 26px;
      animation: spinDisc 5s linear infinite;
      box-shadow: 0 0 15px rgba(79, 168, 255, 0.3);
    }

    @keyframes spinDisc {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }

    .music-title { font-size: 26px; font-weight: 700; color: #ffffff; }
    .music-queue { font-size: 20px; color: var(--text-sub); margin-top: 4px; }
    
    /* 点歌规则与VIP插队清晰指引 */
    .music-tip {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 4px;
      text-align: right;
      white-space: nowrap;
      margin-left: 20px;
    }
    .tip-rule {
      font-size: 19px;
      color: #ffd043;
      font-weight: 800;
      letter-spacing: 0.5px;
    }
    .tip-vip {
      font-size: 16px;
      color: #38ef7d;
      font-weight: 700;
    }

    """
    c = c[:start_idx] + new_music_style + c[end_idx:]

# 2. 移除右下角 HTML 卡片与弹窗，并更新点歌台 HTML
old_html_card_start = "<!-- 7.5 右侧热门点歌单展示卡"
old_html_card_end = "<!-- 8. 底部点歌台 -->"

h_start = c.find(old_html_card_start)
h_end = c.find(old_html_card_end)
if h_start != -1 and h_end != -1:
    c = c[:h_start] + c[h_end:]

# 更新底部点歌台内部 HTML
old_music_bar_html = """    <!-- 8. 底部点歌台 -->
    <div class="music-bar">
      <div class="music-info">
        <div class="music-disc">🎵</div>
        <div>
          <div style="display: flex; align-items: center; gap: 10px;">
            <div class="music-title" id="music-title">♬ 正在播放：《月声尽，心灯明》</div>
            <span class="music-requester" id="music-requester" style="font-size: 18px; color: #ffd043; font-weight: 700;">[由 @晴天 点播]</span>
          </div>
          <div style="display: flex; align-items: center; gap: 14px; margin-top: 5px;">
            <div class="music-progress-container"><div class="music-progress-fill" id="music-progress-fill"></div></div>
            <div class="music-queue" id="music-queue">排队：1. 薛之谦《演员》 · 2. 《东南苦山》</div>
          </div>
        </div>
      </div>
      <div class="music-tip">⭐ 送「为你点亮」VIP插队</div>
    </div>"""

new_music_bar_html = """    <!-- 8. 底部点歌台 (清晰说明点歌需带“点歌”二字与VIP插队特权) -->
    <div class="music-bar">
      <div class="music-info">
        <div class="music-disc">🎵</div>
        <div>
          <div style="display: flex; align-items: center; gap: 10px;">
            <div class="music-title" id="music-title">♬ 正在播放：《月声尽，心灯明》</div>
            <span class="music-requester" id="music-requester" style="font-size: 18px; color: #ffd043; font-weight: 700;">[由 @晴天 点播]</span>
          </div>
          <div style="display: flex; align-items: center; gap: 14px; margin-top: 5px;">
            <div class="music-progress-container"><div class="music-progress-fill" id="music-progress-fill"></div></div>
            <div class="music-queue" id="music-queue">排队：当前无排队 · 发「点歌 歌名」即可点播</div>
          </div>
        </div>
      </div>
      <div class="music-tip">
        <span class="tip-rule">📢 点歌提醒：必须附带“点歌”二字（例：点歌 孤勇者）</span>
        <span class="tip-vip">⭐ 送「为你点亮」VIP极速霸权插队</span>
      </div>
    </div>"""

c = c.replace(old_music_bar_html, new_music_bar_html)

# 3. 移除 initSongGrid 与 toggleSongModal 的无用 JS 函数
c = c.replace("""    // 初始化渲染 24 首完整歌单
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
    }""", "// 歌单已转为界面常驻规则与智能语音引导闭环")

c = c.replace("initSongGrid();\n      ", "")

# 4. 重构 handleDanmakuCommand 中的规则提醒与闭环检测
old_danmaku_command_logic = """      // B. 智能识别：检查该观众是否刚送过【为你点亮】(处于 90 秒 VIP 优先指定窗口)
      if (window.pendingVipUsers && window.pendingVipUsers[user] && (Date.now() - window.pendingVipUsers[user] < 90000)) {
        const extracted = extractSongName(t) || t.replace(/[《》]/g, '').trim();
        delete window.pendingVipUsers[user]; // 成功消费掉 VIP 特权
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

new_danmaku_command_logic = """      // B. VIP特权闭环：检查该观众是否刚送过【为你点亮】(处于 90 秒 VIP 优先指定窗口)
      if (window.pendingVipUsers && window.pendingVipUsers[user] && (Date.now() - window.pendingVipUsers[user] < 90000)) {
        const extracted = extractSongName(t) || (t.includes('点歌') ? t.replace(/.*点歌/, '').trim() : t.replace(/[《》]/g, '').trim());
        delete window.pendingVipUsers[user]; // 消费掉特权
        playNaiwaAudio(ACTION_VOICES.song, `收到【${user}】的VIP指定歌单！已立即插队为你切换到《${extracted}》！`, true);
        handleSongRequest(extracted, user, true);
        return;
      }

      // C. 弹幕点歌闭环检测：严格要求附带“点歌”二字（或带插队特权）
      if (t.includes('点歌') || t.includes('插队')) {
        const songName = extractSongName(t) || t.replace(/.*(点歌|插队)/, '').trim();
        if (songName && songName.length >= 2) {
          const isVip = t.includes('插队') || t.includes('为你点亮');
          handleSongRequest(songName, user, isVip);
          return;
        } else {
          startTalking(`想听什么歌呀？请发送「点歌 歌名」，比如「点歌 孤勇者」，奶娃就帮你排上啦～`);
          return;
        }
      }

      // D. 规则提醒：如果观众发了热门歌名或询问点歌，但未附带“点歌”二字，智能语音提醒规则！
      const isSongKeyword = TRENDING_HOT_SONGS.some(s => t.includes(s.title.replace(/\\(.*?\\)/, '').trim()));
      if (isSongKeyword || t.includes('怎么点') || t.includes('想听歌') || t.includes('来首歌') || t.includes('放首歌')) {
        const example = isSongKeyword ? t : '孤勇者';
        startTalking(`点歌请附带“点歌”二字哦～例如发送「点歌 ${example}」，奶娃才会帮你点播上哦～`);
        return;
      }"""

c = c.replace(old_danmaku_command_logic, new_danmaku_command_logic)

# 5. 更新送出【为你点亮】时的亲口语音，明确提醒“附带点歌二字”
old_vip_prompt = """            const defaultSong = "爱如火 (极乐净土版)";
            handleSongRequest(defaultSong, user, true);
            playNaiwaAudio(ACTION_VOICES.song, `哇！感谢【${user}】送出【为你点亮】！小主人想听什么歌？快在公屏发送歌名，奶娃立刻为你插队换歌哦～`, true);"""

new_vip_prompt = """            const defaultSong = "爱如火 (极乐净土版)";
            handleSongRequest(defaultSong, user, true);
            playNaiwaAudio(ACTION_VOICES.song, `哇！感谢【${user}】送出【为你点亮】！想指定歌曲请在公屏发送「点歌 歌名」（一定要带“点歌”二字哦），奶娃立刻为你插队换歌～`, true);"""

c = c.replace(old_vip_prompt, new_vip_prompt)

# 6. 更新 10 分钟无人点歌时的自动轮播语音，同样带上“附带点歌二字”的提醒闭环
old_auto_dj_prompt = "playNaiwaAudio(ACTION_VOICES.song, `现在直播间空闲啦，奶娃为大家随机挑选了当下热门金曲《${pick.title}》！发「点歌 歌名」可随时插播你想听的歌哦～`);"
new_auto_dj_prompt = "playNaiwaAudio(ACTION_VOICES.song, `现在直播间空闲啦，奶娃为大家随机挑选了当下热门金曲《${pick.title}》！点歌要附带“点歌”二字哦，发送「点歌 歌名」就能排上你的歌啦～`);"
c = c.replace(old_auto_dj_prompt, new_auto_dj_prompt)

with open('douyin_live/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Applied user rule: Removed song card, added '点歌' mandatory reminder & complete loop!")
