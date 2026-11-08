# -*- coding: utf-8 -*-
with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. 替换 case 'balloon' 为 case 'vip_song' 与 case 'balloon'
old_case = """        case 'balloon': // 彩虹气球 (9抖币 · 唯美离地悬浮漂浮)
          playNaiwaAudio(ACTION_VOICES.song, '耶，帅的代名词就是我耶，飞起来啦！', true);
          rig.className = 'character-rig anim-float';
          setEyes('happy');
          setMouth('open');
          spawnGPUParticles('🎈', 35);
          feedRice(1.8);
          showGiftToast('梦幻气球', '彩虹气球', 1.8, '🎈');
          currentActionTimeout = setTimeout(resetToIdle, 2600);
          break;"""

new_case = """        case 'vip_song': // 为你点亮 (9抖币 · 抖音官方礼物对应：VIP特权急速插队点歌)
        case 'balloon':
          const sampleVipSongs = ['爱如火 (极乐净土版)', '狂暴奶龙摇', '朋友的酒', '勇气大爆发', '月声尽，心灯明'];
          const randomSong = sampleVipSongs[Math.floor(Math.random() * sampleVipSongs.length)];
          feedRice(1.8);
          handleSongRequest(randomSong, '榜一大哥', true);
          break;"""

c = c.replace(old_case, new_case)

# 2. 优化点歌台排版，防止文字折行重叠
old_tip_html = '<div class="music-tip">发「点歌 歌名」排队 · 送「为你点亮」VIP插队</div>'
new_tip_html = '<div class="music-tip">⭐ 送「为你点亮」VIP插队</div>'
c = c.replace(old_tip_html, new_tip_html)

# 3. 优化点歌台 CSS 防止文本溢出
old_music_css = """.music-bar {
      position: absolute;
      bottom: 60px;
      left: 50px;
      right: 50px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      backdrop-filter: blur(12px);
      border-radius: 24px;
      padding: 20px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 20;
    }

    .music-info { display: flex; align-items: center; gap: 16px; }"""

new_music_css = """.music-bar {
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
    .music-tip { font-size: 20px; color: var(--accent-yellow); font-weight: 700; white-space: nowrap; margin-left: 15px; }"""

c = c.replace(old_music_css, new_music_css)

with open('douyin_live/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated index.html with VIP song logic & music bar layout!")
