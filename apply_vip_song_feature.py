# -*- coding: utf-8 -*-
with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. 更新右侧礼物按钮：为你点亮 -> 9抖币·插队点歌
old_tag = """      <div class="action-tag" onclick="triggerAction('balloon')">
        <span class="action-text">为你点亮 <span class="coin-badge">9抖币</span></span>
        <img class="action-icon-img" src="assets/gifts/zhaixing.png" alt="为你点亮">
      </div>"""

new_tag = """      <div class="action-tag" onclick="triggerAction('vip_song')" title="送【为你点亮】享受VIP极速插队点歌特权">
        <span class="action-text">为你点亮 <span class="coin-badge gold">9抖币·插队点歌</span></span>
        <img class="action-icon-img" src="assets/gifts/zhaixing.png" alt="为你点亮">
      </div>"""

c = c.replace(old_tag, new_tag)

# 2. 更新底部点歌台提示语
c = c.replace(
    '<div class="music-tip">发「点歌 歌名」点歌</div>',
    '<div class="music-tip">发「点歌 歌名」排队 · 送「为你点亮」VIP插队</div>'
)

# 3. 更新导演台按钮
c = c.replace(
    '<button class="ctrl-btn" onclick="triggerAction(\'balloon\')">⭐ 为你点亮 9抖币</button>',
    '<button class="ctrl-btn special" onclick="triggerAction(\'vip_song\')">⭐ 为你点亮 9抖币 (VIP插队点歌)</button>'
)

# 4. 更新 triggerAction 中的 case
old_balloon_case = """        case 'balloon': // 为你点亮 (9抖币)
          playNaiwaAudio(ACTION_VOICES.song, '星光点亮啦！帅气飞天咯～', true);
          rig.className = 'character-rig anim-float';
          setEyes('star');
          setMouth('open');
          spawnGPUParticles('⭐', 35);
          spawnGPUParticles('✨', 25);
          feedRice(1.8);
          showGiftToast('梦幻守护', '为你点亮', 1.8, '⭐');
          currentActionTimeout = setTimeout(resetToIdle, 2600);
          break;"""

new_balloon_case = """        case 'vip_song': // 为你点亮 (9抖币 · 抖音官方礼物对应：VIP特权急速插队点歌)
        case 'balloon':
          const sampleVipSongs = ['爱如火 (极乐净土版)', '狂暴奶龙摇', '朋友的酒', '勇气大爆发', '月声尽，心灯明'];
          const randomSong = sampleVipSongs[Math.floor(Math.random() * sampleVipSongs.length)];
          feedRice(1.8);
          handleSongRequest(randomSong, '榜一大哥', true);
          break;"""

c = c.replace(old_balloon_case, new_balloon_case)

# 5. 更新 handleSongRequest 支持 VIP 插队与立即切歌，以及 updateMusicUI 的 VIP 徽章
old_song_func = """    // 观众点歌核心处理函数
    function handleSongRequest(songName, userName = "热心观众") {
      const cleanName = songName.replace(/^(点歌|播放|想听)/, '').trim();
      if (!cleanName) return;

      // 构造歌曲条目 (自动轮转内置音源与伴奏流)
      const trackSrc = requestQueue.length % 2 === 0 ? "music/happy_chibi_bgm.mp3" : "music/sweet_lullaby_bgm.mp3";
      const newSong = {
        title: cleanName,
        artist: "Q版伴奏",
        src: trackSrc,
        user: userName
      };

      requestQueue.push(newSong);

      // 奶娃触发点歌语音和跳舞反馈
      playNaiwaAudio(ACTION_VOICES.song, `好听好听！${userName}点的《${cleanName}》排上啦，马上给哥哥姐姐放～`);
      triggerAction('dance');
      spawnGPUParticles('🎵', 20);

      // 如果当前没有在播，立即启动
      if (!isPlaying) {
        playNext();
      } else {
        updateMusicUI();
      }

      addDanmaku(userName, `[点了歌曲 《${cleanName}》]`, true);
    }"""

new_song_func = """    // 观众点歌核心处理函数 (全面支持免费弹幕排队与【为你点亮】9抖币 VIP 极速插队)
    function handleSongRequest(songName, userName = "热心观众", isPriority = false) {
      const cleanName = songName.replace(/^(点歌|播放|想听|插队点歌|VIP点歌)/, '').trim() || "特别好听的专属歌";

      // 构造歌曲条目 (自动轮转内置音源与伴奏流)
      const trackSrc = requestQueue.length % 2 === 0 ? "music/happy_chibi_bgm.mp3" : "music/sweet_lullaby_bgm.mp3";
      const newSong = {
        title: cleanName,
        artist: isPriority ? "👑 VIP专属插队" : "Q版伴奏",
        src: trackSrc,
        user: userName,
        isPriority: isPriority
      };

      if (isPriority) {
        // 【VIP 插队特权】：立即插入队列第 1 位并直接切歌播放！
        requestQueue.unshift(newSong);
        playNext();

        // 视听大动效反馈：星光升空漂浮 + 音符金光粒子爆发 + 亲口语音欢呼感谢
        playNaiwaAudio(ACTION_VOICES.song, `哇！收到【为你点亮】啦！感谢${userName}开启VIP专属通道，已立刻插队播放《${cleanName}》～`, true);
        rig.className = 'character-rig anim-float';
        setEyes('star');
        setMouth('open');
        spawnGPUParticles('⭐', 35);
        spawnGPUParticles('🎵', 30);
        showGiftToast(userName, '为你点亮 · 插队点歌', 1.8, '👑');
        addDanmaku(userName, `[👑 送出【为你点亮】VIP插队 《${cleanName}》]`, true);
        currentActionTimeout = setTimeout(resetToIdle, 2800);
      } else {
        // 普通排队点歌：进入排队队列末尾
        requestQueue.push(newSong);
        playNaiwaAudio(ACTION_VOICES.song, `好听好听！${userName}点的《${cleanName}》排上啦，马上给哥哥姐姐放～`);
        rig.className = 'character-rig anim-dance';
        setEyes('happy');
        setMouth('open');
        spawnGPUParticles('🎵', 20);
        addDanmaku(userName, `[点了歌曲 《${cleanName}》]`, true);
        currentActionTimeout = setTimeout(resetToIdle, 2200);

        if (!isPlaying) {
          playNext();
        } else {
          updateMusicUI();
        }
      }
    }"""

c = c.replace(old_song_func, new_song_func)

# 6. 更新 updateMusicUI 增加 VIP 标识
old_music_ui = """      if (currentTrack) {
        musicTitle.innerText = `♬ 正在播放：《${currentTrack.title}》`;
        const reqEl = document.getElementById('music-requester');
        if (reqEl) {
          reqEl.innerText = `[由 @${currentTrack.user || '晴天'} 点播]`;
        }
      }"""

new_music_ui = """      if (currentTrack) {
        if (currentTrack.isPriority) {
          musicTitle.innerHTML = `♬ 正在播放：<span style="color: #ffd043; font-weight: 800;">《${currentTrack.title}》</span> <span style="background: linear-gradient(135deg, #ff9800, #ff5722); color: #fff; padding: 2px 8px; border-radius: 10px; font-size: 16px; font-weight: 800; vertical-align: middle;">👑 VIP插队</span>`;
        } else {
          musicTitle.innerText = `♬ 正在播放：《${currentTrack.title}》`;
        }
        const reqEl = document.getElementById('music-requester');
        if (reqEl) {
          reqEl.innerText = `[由 @${currentTrack.user || '晴天'} 点播]`;
        }
      }"""

c = c.replace(old_music_ui, new_music_ui)

# 7. 弹幕检测中加入插队点歌检测
old_danmaku_check = """      if (t.startsWith('点歌') || t.startsWith('播放') || t.startsWith('想听')) {
        handleSongRequest(t, user);
        return;
      }"""

new_danmaku_check = """      if (t.includes('插队') || t.includes('为你点亮')) {
        handleSongRequest(t, user, true);
        return;
      }
      if (t.startsWith('点歌') || t.startsWith('播放') || t.startsWith('想听')) {
        handleSongRequest(t, user, false);
        return;
      }"""

c = c.replace(old_danmaku_check, new_danmaku_check)

with open('douyin_live/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Applied VIP Song Request feature for 为你点亮!")
