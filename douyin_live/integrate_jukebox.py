import os

index_path = r'D:\zhibo\Open-LLM-VTuber\douyin_live\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add audio element and jukebox UI enhancements
audio_tag = '<audio id="bgm-player" preload="auto"></audio>'

if 'id="bgm-player"' not in html:
    html = html.replace('<body>', '<body>\n  ' + audio_tag)

# 2. Add volume slider & custom request input in the director panel
old_panel_btns = '<button class="ctrl-btn" onclick="mockDanmaku()">📩 模拟弹幕送礼</button>'
new_panel_btns = '''<button class="ctrl-btn" onclick="mockDanmaku()">📩 模拟弹幕送礼</button>
      <button class="ctrl-btn special" id="btn-play-toggle" onclick="toggleBgmPlay()">🎵 播放/暂停BGM</button>
      <button class="ctrl-btn" onclick="skipSong()">⏭️ 切下一首</button>
    </div>
    <div style="margin-top: 12px; margin-bottom: 12px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 12px;">
      <div style="display: flex; justify-content: space-between; font-size: 15px; color: #ffd043; margin-bottom: 6px;">
        <span>🔊 BGM 音量调节</span>
        <span id="vol-text">35%</span>
      </div>
      <input type="range" id="bgm-vol" min="0" max="100" value="35" style="width: 100%; cursor: pointer;" oninput="setBgmVolume(this.value)">
    </div>
    <div style="display: flex; gap: 8px; margin-bottom: 14px;">
      <input type="text" id="request-input" placeholder="输入歌名 (如: 朋友的酒)" style="flex: 1; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 8px 12px; color: #fff; font-size: 14px;" onkeydown="if(event.key==='Enter') testRequestSong()">
      <button class="ctrl-btn" style="padding: 8px 14px; font-size: 14px;" onclick="testRequestSong()">🎤 点歌</button>'''

html = html.replace(old_panel_btns, new_panel_btns)

# 3. Add Jukebox JavaScript Engine
jukebox_js = '''
    // =======================================================
    // 智能点歌台与背景音乐播放系统 (Web Audio Jukebox)
    // =======================================================
    const bgmPlayer = document.getElementById('bgm-player');
    const musicTitle = document.getElementById('music-title');
    const musicQueue = document.getElementById('music-queue');
    const musicDisc = document.querySelector('.music-disc');
    const btnPlayToggle = document.getElementById('btn-play-toggle');

    // 默认常驻伴奏曲库
    const defaultPlaylist = [
      { title: "软糖华尔兹 (Q版伴奏)", artist: "奶娃小乐队", src: "music/happy_chibi_bgm.wav", user: "系统" },
      { title: "摇篮小夜曲 (八音盒)", artist: "甜心纯音", src: "music/sweet_lullaby_bgm.wav", user: "系统" }
    ];

    let currentTrack = null;
    let defaultIndex = 0;
    let requestQueue = []; // 观众点歌插队队列
    let isPlaying = false;

    // 初始化播放器音量
    bgmPlayer.volume = 0.35;

    // 播放下一首逻辑
    function playNext() {
      if (requestQueue.length > 0) {
        // 优先播放观众点的歌
        currentTrack = requestQueue.shift();
      } else {
        // 播放默认伴奏循环
        currentTrack = defaultPlaylist[defaultIndex];
        defaultIndex = (defaultIndex + 1) % defaultPlaylist.length;
      }

      bgmPlayer.src = currentTrack.src;
      bgmPlayer.play().then(() => {
        isPlaying = true;
        updateMusicUI();
      }).catch(err => {
        console.log("浏览器等待用户交互后播放音频:", err);
        isPlaying = false;
        updateMusicUI();
      });
    }

    // 播放完毕自动切下一首
    bgmPlayer.onended = function() {
      playNext();
    };

    // 刷新点歌台界面
    function updateMusicUI() {
      if (currentTrack) {
        musicTitle.innerText = `♬ 正在播放：《${currentTrack.title}》`;
        if (currentTrack.user && currentTrack.user !== "系统") {
          musicTitle.innerText += ` · 点歌人: ${currentTrack.user}`;
        }
      }

      if (requestQueue.length > 0) {
        const queueNames = requestQueue.slice(0, 2).map((item, idx) => `${idx + 1}. 《${item.title}》· ${item.user}`);
        musicQueue.innerText = `排队：${queueNames.join(' · ')} (共${requestQueue.length}首)`;
      } else {
        musicQueue.innerText = "当前无排队 · 发「点歌 歌名」即可点歌";
      }

      // 唱片机转动状态
      if (isPlaying) {
        musicDisc.style.animationPlayState = 'running';
        if (btnPlayToggle) btnPlayToggle.innerText = '⏸️ 暂停BGM';
      } else {
        musicDisc.style.animationPlayState = 'paused';
        if (btnPlayToggle) btnPlayToggle.innerText = '▶️ 播放BGM';
      }
    }

    // 观众点歌核心处理函数
    function handleSongRequest(songName, userName = "热心观众") {
      const cleanName = songName.replace(/^(点歌|播放|想听)/, '').trim();
      if (!cleanName) return;

      // 构造歌曲条目 (自动轮转内置音源与伴奏流)
      const trackSrc = requestQueue.length % 2 === 0 ? "music/happy_chibi_bgm.wav" : "music/sweet_lullaby_bgm.wav";
      const newSong = {
        title: cleanName,
        artist: "Q版伴奏",
        src: trackSrc,
        user: userName
      };

      requestQueue.push(newSong);

      // 奶娃触发点歌语音和跳舞反馈
      setSpeech(`好听好听！${userName}点的《${cleanName}》排上啦，马上给哥哥姐姐放～`);
      triggerAction('dance');
      spawnGPUParticles('🎵', 20);

      // 如果当前没有在播，立即启动
      if (!isPlaying) {
        playNext();
      } else {
        updateMusicUI();
      }

      addDanmaku(userName, `[点了歌曲 《${cleanName}》]`, true);
    }

    // 播放/暂停切换
    function toggleBgmPlay() {
      if (isPlaying) {
        bgmPlayer.pause();
        isPlaying = false;
        updateMusicUI();
      } else {
        if (!currentTrack) {
          playNext();
        } else {
          bgmPlayer.play().then(() => {
            isPlaying = true;
            updateMusicUI();
          });
        }
      }
    }

    // 切歌
    function skipSong() {
      playNext();
    }

    // 音量调节
    function setBgmVolume(val) {
      bgmPlayer.volume = val / 100.0;
      document.getElementById('vol-text').innerText = `${val}%`;
    }

    // 测试点歌输入
    function testRequestSong() {
      const input = document.getElementById('request-input');
      const val = input.value.trim();
      if (val) {
        handleSongRequest(val, "榜一大哥");
        input.value = "";
      }
    }

    // 弹幕识别中加入点歌检测
    const origHandleDanmaku = handleDanmakuCommand;
    handleDanmakuCommand = function(user, text) {
      const t = text.trim();
      if (t.startsWith('点歌') || t.startsWith('播放') || t.startsWith('想听')) {
        handleSongRequest(t, user);
        return;
      }
      origHandleDanmaku(user, text);
    };

    // 页面加载后自动开启第一首伴奏
    setTimeout(() => {
      playNext();
    }, 800);
'''

# Insert jukebox js before </body>
html = html.replace('</script>\n</body>', jukebox_js + '\n  </script>\n</body>')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Jukebox system successfully integrated into index.html!")
