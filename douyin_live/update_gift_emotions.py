# -*- coding: utf-8 -*-
import shutil

html_path = 'D:/zhibo/Open-LLM-VTuber/douyin_live/index.html'
bak_path = 'D:/zhibo/Open-LLM-VTuber/douyin_live/index.html.bak'

# 从备份还原干净的基础版本
shutil.copyfile(bak_path, html_path)
print("Restored clean backup from", bak_path)

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 统一全部为 \n
content = content.replace('\r\n', '\n')

# 1. 修复 shadowBellyExpand 并增加 5 大专属定制动作动画
target_shadow = """    /* 膨胀时地影同步扩大，落地重量感十足 */
    .shadow-belly-laugh {
      animation: shadowBellyExpand 9.2s cubic-bezier(0.25, 1, 0.5, 1) forwards !important;
    }
    @keyframes shadowBellyExpand {
      0%, 100% { transform: scale(1); opacity: 0.25; }
      5%, 90% { transform: scale(1.45); opacity: 0.55; }
    }
      12%, 84% { transform: scale(1.45); opacity: 0.45; }
    }"""

replacement_shadow = """    /* 膨胀时地影同步扩大，落地重量感十足 */
    .shadow-belly-laugh {
      animation: shadowBellyExpand 9.2s cubic-bezier(0.25, 1, 0.5, 1) forwards !important;
    }
    @keyframes shadowBellyExpand {
      0%, 100% { transform: scale(1); opacity: 0.25; }
      5%, 90% { transform: scale(1.45); opacity: 0.55; }
      12%, 84% { transform: scale(1.45); opacity: 0.45; }
    }

    /* 心跳小鹿乱撞 (小心心专属 · 节奏胸口律动膨胀) */
    .anim-heartbeat {
      animation: heartbeatPulse 1.8s cubic-bezier(0.25, 0.8, 0.25, 1) forwards !important;
    }
    @keyframes heartbeatPulse {
      0%, 100% { transform: scale(1, 1); }
      14% { transform: scale(1.18, 0.92) translateY(6px); }
      28% { transform: scale(0.94, 1.08) translateY(-16px); }
      42% { transform: scale(1.14, 0.93) translateY(4px); }
      56% { transform: scale(0.97, 1.03) translateY(-6px); }
      70% { transform: scale(1.05, 0.96) translateY(2px); }
      85% { transform: scale(1, 1); }
    }

    /* 浪漫飞吻深情鞠躬 (玫瑰专属 · 前倾鞠躬后探头送吻) */
    .anim-kiss {
      animation: kissBow 2.4s cubic-bezier(0.34, 1.3, 0.64, 1) forwards !important;
    }
    @keyframes kissBow {
      0% { transform: scale(1, 1) rotate(0deg) translateY(0); }
      20% { transform: scale(1.08, 0.92) rotate(-9deg) translateY(20px); }
      45% { transform: scale(0.95, 1.08) rotate(7deg) translateY(-26px); }
      70% { transform: scale(1.04, 0.96) rotate(-2deg) translateY(-8px); }
      85% { transform: scale(0.98, 1.02) rotate(1deg) translateY(0); }
      100% { transform: scale(1, 1) rotate(0deg) translateY(0); }
    }

    /* 微醺晃荡与饱嗝 (大啤酒专属 · 软糖醉酒晃动后大嗝) */
    .anim-drunk {
      animation: drunkWobble 2.6s ease-in-out forwards !important;
    }
    @keyframes drunkWobble {
      0% { transform: scale(1, 1) rotate(0deg); }
      15% { transform: scale(1.06, 0.94) rotate(-14deg) translateY(12px); }
      30% { transform: scale(0.94, 1.06) rotate(14deg) translateY(-8px); }
      45% { transform: scale(1.1, 0.9) rotate(-10deg) translateY(10px); }
      60% { transform: scale(0.96, 1.04) rotate(8deg) translateY(-4px); }
      75% { transform: scale(1.24, 0.8) rotate(0deg) translateY(26px); }
      85% { transform: scale(0.9, 1.16) translateY(-32px); }
      100% { transform: scale(1, 1) rotate(0deg) translateY(0); }
    }

    /* 超能爱心光波大发射 (手势比心专属 · 蓄力猛烈冲击) */
    .anim-heart-beam {
      animation: heartBeamRecoil 2.4s cubic-bezier(0.2, 0.9, 0.3, 1.2) forwards !important;
    }
    @keyframes heartBeamRecoil {
      0% { transform: scale(1, 1) translateY(0); }
      15% { transform: scale(0.86, 1.16) translateY(-22px); }
      30% { transform: scale(1.38, 0.76) translateY(38px); }
      50% { transform: scale(0.92, 1.12) translateY(-18px); }
      70% { transform: scale(1.08, 0.94) translateY(6px); }
      100% { transform: scale(1, 1) translateY(0); }
    }

    /* 活力应援高呼 (人气票专属 · 连续小跳步挥臂) */
    .anim-cheer {
      animation: cheerJumps 2.2s ease-in-out forwards !important;
    }
    @keyframes cheerJumps {
      0%, 100% { transform: scale(1, 1) translateY(0) rotate(0deg); }
      15% { transform: scale(0.9, 1.18) translateY(-75px) rotate(-6deg); }
      30% { transform: scale(1.15, 0.88) translateY(0) rotate(4deg); }
      45% { transform: scale(0.92, 1.14) translateY(-60px) rotate(-4deg); }
      60% { transform: scale(1.1, 0.92) translateY(0) rotate(2deg); }
      75% { transform: scale(0.96, 1.06) translateY(-25px) rotate(0deg); }
    }"""

assert target_shadow in content, "target_shadow not found"
content = content.replace(target_shadow, replacement_shadow)
print("1. Replaced shadow and added keyframes.")

# 2. 增加氛围滤镜层 CSS
target_style_end = """    .music-progress-fill {
      width: 0%;
      height: 100%;
      background: linear-gradient(90deg, #4fa8ff, #ffd043);
      border-radius: 3px;
      transition: width 0.3s;
    }

  </style>"""

replacement_style_end = """    .music-progress-fill {
      width: 0%;
      height: 100%;
      background: linear-gradient(90deg, #4fa8ff, #ffd043);
      border-radius: 3px;
      transition: width 0.3s;
    }

    /* 全屏氛围滤镜与光效层 */
    .atmosphere-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 18;
      opacity: 0;
      transition: opacity 0.4s ease;
    }
    .atmosphere-overlay.drunk-mode {
      opacity: 1;
      background: radial-gradient(circle at 50% 60%, rgba(255, 180, 0, 0.15) 0%, rgba(255, 120, 0, 0.42) 85%);
      animation: drunkVignettePulse 2s infinite ease-in-out;
    }
    @keyframes drunkVignettePulse {
      0%, 100% { filter: blur(0px); opacity: 0.85; }
      50% { filter: blur(2px); opacity: 0.95; }
    }
    .atmosphere-overlay.love-mode {
      opacity: 1;
      background: radial-gradient(circle at 50% 50%, rgba(255, 105, 180, 0.25) 0%, rgba(255, 20, 147, 0.38) 90%);
      animation: lovePulse 1.8s ease-in-out;
    }
    @keyframes lovePulse {
      0% { opacity: 0; transform: scale(0.9); }
      30% { opacity: 0.9; transform: scale(1.05); }
      100% { opacity: 0; transform: scale(1.2); }
    }
    .atmosphere-overlay.gold-vip-mode {
      opacity: 1;
      background: radial-gradient(circle at 50% 30%, rgba(255, 215, 0, 0.35) 0%, rgba(255, 140, 0, 0.12) 60%, transparent 80%);
      animation: goldVipGlow 2.5s ease-in-out;
    }
    @keyframes goldVipGlow {
      0% { opacity: 0; }
      40% { opacity: 0.9; }
      100% { opacity: 0; }
    }

  </style>"""

assert target_style_end in content, "target_style_end not found"
content = content.replace(target_style_end, replacement_style_end)
print("2. Added atmosphere overlay CSS.")

# 3. 增加 sfx-player audio 标签与 atmosphere-overlay div
target_audio = """  <audio id="bgm-player" preload="auto"></audio>
  <audio id="voice-player" preload="auto"></audio>

  <!-- 视口受击震屏容器 -->
  <div id="viewport-container">

    <!-- GPU加速的丝滑散落特效层 (取代容易卡顿的1080x1920 Canvas) -->
    <div id="fx-container"></div>"""

replacement_audio = """  <audio id="bgm-player" preload="auto"></audio>
  <audio id="voice-player" preload="auto"></audio>
  <audio id="sfx-player" preload="auto"></audio>

  <!-- 视口受击震屏容器 -->
  <div id="viewport-container">

    <!-- 全屏氛围滤镜与光效层 -->
    <div id="atmosphere-overlay" class="atmosphere-overlay"></div>

    <!-- GPU加速的丝滑散落特效层 (取代容易卡顿的1080x1920 Canvas) -->
    <div id="fx-container"></div>"""

assert target_audio in content, "target_audio not found"
content = content.replace(target_audio, replacement_audio)
print("3. Added sfx-player and atmosphere-overlay div.")

# 4. 注册 eyes.heart 素材
target_rig_eyes = """      eyes: {
        default: 'assets/rig/pupils_default.png',
        happy: 'assets/rig/eyes_happy.png',
        dizzy: 'assets/rig/eyes_dizzy.png',
        star: 'assets/rig/eyes_star.png'
      },"""

replacement_rig_eyes = """      eyes: {
        default: 'assets/rig/pupils_default.png',
        happy: 'assets/rig/eyes_happy.png',
        dizzy: 'assets/rig/eyes_dizzy.png',
        star: 'assets/rig/eyes_star.png',
        heart: 'assets/rig/eyes_heart.png'
      },"""

assert target_rig_eyes in content, "target_rig_eyes not found"
content = content.replace(target_rig_eyes, replacement_rig_eyes)
print("4. Registered eyes.heart.")

# 5. 增加 sfxPlayer 播放辅助函数和 setAtmosphere 辅助函数
target_script_start = """    window.pendingVipUsers = {};
    const viewport = document.getElementById('viewport-container');"""

replacement_script_start = """    window.pendingVipUsers = {};
    const viewport = document.getElementById('viewport-container');
    const sfxPlayer = document.getElementById('sfx-player');
    const atmosphereOverlay = document.getElementById('atmosphere-overlay');
    let sfxVolume = 1.0;
    if (sfxPlayer) sfxPlayer.volume = sfxVolume;

    // 专属拟声音效播放器 (独立多声道，绝不抢占语音或BGM)
    function playSFX(sfxPath) {
      unlockAudioContext();
      if (!sfxPlayer) return;
      try {
        sfxPlayer.pause();
        sfxPlayer.currentTime = 0;
      } catch(e) {}
      sfxPlayer.src = sfxPath;
      sfxPlayer.play().catch(err => {
        console.warn("SFX play auto-blocked:", err);
      });
    }

    // 全屏沉浸氛围调节器
    function setAtmosphere(mode, duration = 2400) {
      if (!atmosphereOverlay) return;
      atmosphereOverlay.className = `atmosphere-overlay ${mode}`;
      setTimeout(() => {
        if (atmosphereOverlay && atmosphereOverlay.className.includes(mode)) {
          atmosphereOverlay.className = 'atmosphere-overlay';
        }
      }, duration);
    }"""

assert target_script_start in content, "target_script_start not found"
content = content.replace(target_script_start, replacement_script_start)
print("5. Added sfxPlayer & setAtmosphere.")

# 6. 更新 resetToIdle 清理氛围
target_reset_idle = """      setEyes('default');
      setMouth('neutral');
      layerBlush.style.opacity = '0';
      sleepBubble.classList.remove('active');
      const eq = document.getElementById('audio-equalizer');
      if (eq) eq.classList.remove('active');
    }"""

replacement_reset_idle = """      setEyes('default');
      setMouth('neutral');
      layerBlush.style.opacity = '0';
      sleepBubble.classList.remove('active');
      if (atmosphereOverlay) atmosphereOverlay.className = 'atmosphere-overlay';
      const eq = document.getElementById('audio-equalizer');
      if (eq) eq.classList.remove('active');
    }"""

assert target_reset_idle in content, "target_reset_idle not found"
content = content.replace(target_reset_idle, replacement_reset_idle)
print("6. Updated resetToIdle.")

# 7. 彻底升级 triggerAction 函数为 10 大定制心意闭环动作
start_idx = content.find("    // 动作与特效触发调度 (保留所有丝滑粒子与物理动效)")
end_idx = content.find("    // =======================================================\n    // 奶娃真实高保真语音驱动引擎")
assert start_idx != -1 and end_idx != -1, "triggerAction boundaries not found"

new_trigger_section = """    // 动作与特效触发调度 (全面升级：10大官方礼物专属定制心意、拟声音效、专属动作与全屏氛围)
    function triggerAction(action, user = '热心老铁', fromGiftEvent = false) {
      if (isTalking) stopTalking();
      if (currentActionTimeout) clearTimeout(currentActionTimeout);
      if (sleepBubble) sleepBubble.classList.remove('active');
      if (atmosphereOverlay) atmosphereOverlay.className = 'atmosphere-overlay';

      // 切换动作时保证之前大笑视频安全停止
      const runningVideo = document.getElementById('video-action-player');
      if (runningVideo && action !== 'belly_laugh') {
        runningVideo.classList.remove('active');
        try { runningVideo.pause(); } catch(e) {}
        rig.style.opacity = '1';
        rig.style.transform = '';
      }

      switch(action) {
        // -------------------------------------------------------------
        // 1. 小心心 (1抖币 · 专属动作：心跳小鹿乱撞 · 砰砰双重心跳音效)
        // -------------------------------------------------------------
        case 'blush':
          playSFX('assets/sfx/heartbeat.wav');
          playNaiwaAudio(ACTION_VOICES.blush, `哇！谢谢【${user}】哥哥的小心心，奶娃心里小鹿乱撞，扑通扑通跳个不停呢～`, true);
          rig.className = 'character-rig anim-heartbeat';
          setEyes('happy');
          setMouth('open');
          layerBlush.style.opacity = '1';
          setAtmosphere('love-mode', 2200);
          spawnGPUParticles('💖', 35);
          spawnGPUParticles('💕', 15);
          if (!fromGiftEvent) {
            feedRice(0.2);
            showGiftToast(user, '小心心', 0.2, '💖');
          }
          currentActionTimeout = setTimeout(resetToIdle, 2600);
          break;

        // -------------------------------------------------------------
        // 2. 抖音 (1抖币 · 专属动作：潮流音符蹦跳舞 · 欢快礼花声)
        // -------------------------------------------------------------
        case 'boing':
          playSFX('assets/sfx/confetti.wav');
          playNaiwaAudio(ACTION_VOICES.boing, `收到【${user}】老铁的抖音专属音符！一起跟着节拍摇摆起来～`, true);
          rig.className = 'character-rig anim-boing';
          setEyes('happy');
          setMouth('open');
          spawnGPUParticles('🎵', 30);
          spawnGPUParticles('✨', 25);
          if (!fromGiftEvent) {
            feedRice(0.2);
            showGiftToast(user, '抖音', 0.2, '🎵');
          }
          currentActionTimeout = setTimeout(resetToIdle, 2200);
          break;

        // -------------------------------------------------------------
        // 3. 玫瑰 (1抖币 · 专属动作：浪漫飞吻深情鞠躬 · 啵唧飞吻浪漫银铃)
        // -------------------------------------------------------------
        case 'rose':
          playSFX('assets/sfx/kiss.wav');
          playNaiwaAudio(ACTION_VOICES.song, `哇！好浪漫的玫瑰花！啵唧～奶娃送给【${user}】哥哥一个超级甜蜜的飞吻！`, true);
          rig.className = 'character-rig anim-kiss';
          setEyes('happy');
          setMouth('o');
          layerBlush.style.opacity = '0.9';
          setTimeout(() => setMouth('open'), 700);
          setAtmosphere('love-mode', 2500);
          spawnGPUParticles('🌹', 35);
          spawnGPUParticles('💖', 20);
          if (!fromGiftEvent) {
            feedRice(0.2);
            showGiftToast(user, '玫瑰', 0.2, '🌹');
          }
          currentActionTimeout = setTimeout(resetToIdle, 2600);
          break;

        // -------------------------------------------------------------
        // 4. 人气票 (1抖币 · 专属动作：活力应援高呼 · 礼炮开香槟叮当)
        // -------------------------------------------------------------
        case 'praise':
          playSFX('assets/sfx/confetti.wav');
          playNaiwaAudio(ACTION_VOICES.song, `人气暴涨！万分感谢【${user}】投出宝贵的人气票，奶娃冲鸭冲榜一！`, true);
          rig.className = 'character-rig anim-cheer';
          setEyes('star');
          setMouth('open');
          spawnGPUParticles('🎟️', 30);
          spawnGPUParticles('🎉', 25);
          spawnGPUParticles('✨', 20);
          if (!fromGiftEvent) {
            feedRice(0.2);
            showGiftToast(user, '人气票', 0.2, '🎟️');
          }
          currentActionTimeout = setTimeout(resetToIdle, 2400);
          break;

        // -------------------------------------------------------------
        // 5. 大啤酒 (2抖币 · 专属动作：微醺摇摆醉打饱嗝 · 吨吨咽酒与爆笑大嗝)
        // -------------------------------------------------------------
        case 'pijiu':
          playSFX('assets/sfx/beer_chug.wav');
          playNaiwaAudio(ACTION_VOICES.hungry, `哈～好爽快的大啤酒！【${user}】大哥豪气！吨吨吨……嗝～奶娃有点飘飘然啦～`, true);
          rig.className = 'character-rig anim-drunk';
          setEyes('dizzy');
          setMouth('o');
          layerBlush.style.opacity = '1';
          setAtmosphere('drunk-mode', 3000);
          spawnGPUParticles('🍺', 28);
          spawnGPUParticles('🫧', 25);
          setTimeout(() => {
            triggerScreenShake();
            setMouth('open');
          }, 1800);
          if (!fromGiftEvent) {
            feedRice(0.4);
            showGiftToast(user, '大啤酒', 0.4, '🍺');
          }
          currentActionTimeout = setTimeout(resetToIdle, 2800);
          break;

        // -------------------------------------------------------------
        // 6. 你最好看 (2抖币 · 专属动作：眼冒桃心小迷妹 · 专绘双粉心瞳孔)
        // -------------------------------------------------------------
        case 'haokan':
          playSFX('assets/sfx/sparkle_camera.wav');
          playNaiwaAudio(ACTION_VOICES.song, `眼里全是你！【${user}】在奶娃眼里是全宇宙最好看、最帅气的小可爱！`, true);
          rig.className = 'character-rig anim-dance';
          setEyes('heart');
          setMouth('open');
          layerBlush.style.opacity = '1';
          setAtmosphere('love-mode', 2200);
          spawnGPUParticles('✨', 35);
          spawnGPUParticles('💖', 25);
          if (!fromGiftEvent) {
            feedRice(0.4);
            showGiftToast(user, '你最好看', 0.4, '✨');
          }
          currentActionTimeout = setTimeout(resetToIdle, 2600);
          break;

        // -------------------------------------------------------------
        // 7. 手势比心 (5抖币 · 专属动作：超能爱心光波大发射 · 激光充能轰鸣)
        // -------------------------------------------------------------
        case 'hearts':
          playSFX('assets/sfx/heart_beam.wav');
          playNaiwaAudio(ACTION_VOICES.song, `收到超级大爱心！奶娃超能爱心光波——发射！【${user}】要接住满满的幸福哦！`, true);
          rig.className = 'character-rig anim-heart-beam';
          setEyes('happy');
          setMouth('o');
          layerBlush.style.opacity = '0.9';
          setTimeout(() => {
            triggerScreenShake();
            setMouth('open');
            spawnGPUParticles('💘', 35);
            spawnGPUParticles('💥', 20);
          }, 650);
          setAtmosphere('love-mode', 2400);
          if (!fromGiftEvent) {
            feedRice(1.0);
            showGiftToast(user, '手势比心', 1.0, '🫰');
          }
          currentActionTimeout = setTimeout(resetToIdle, 2700);
          break;

        // -------------------------------------------------------------
        // 8. 为你点亮 (9抖币 · 专属功能：VIP星光加冕 + 霸权插队点歌 · 天使竖琴交响)
        // -------------------------------------------------------------
        case 'vip_song':
        case 'balloon':
          playSFX('assets/sfx/crown_shimmer.wav');
          rig.className = 'character-rig anim-float';
          setEyes('star');
          setMouth('open');
          setAtmosphere('gold-vip-mode', 2800);
          spawnGPUParticles('⭐', 35);
          spawnGPUParticles('👑', 15);
          spawnGPUParticles('🎵', 25);
          if (!fromGiftEvent) {
            const sampleVipSongs = ['爱如火 (极乐净土版)', '狂暴奶龙摇', '朋友的酒', '勇气大爆发', '月声尽，心灯明'];
            const randomSong = sampleVipSongs[Math.floor(Math.random() * sampleVipSongs.length)];
            feedRice(1.8);
            handleSongRequest(randomSong, user, true);
          }
          break;

        // -------------------------------------------------------------
        // 9. 甜甜圈 (10抖币 · 专属动作：一口吞膨胀肚皮 DuangDuang 弹 · 嗷呜吞咽弹性duang)
        // -------------------------------------------------------------
        case 'donut':
          playSFX('assets/sfx/donut_eat.wav');
          playNaiwaAudio(ACTION_VOICES.hungry, `嗷呜——！好大好香的甜甜圈！【${user}】喂饱饱啦，奶娃的肚子变得圆滚滚像个小气球啦！`, true);
          rig.className = 'character-rig anim-bloat';
          setEyes('happy');
          setMouth('o');
          setTimeout(() => setMouth('open'), 850);
          spawnGPUParticles('🍩', 35);
          spawnGPUParticles('✨', 20);
          if (!fromGiftEvent) {
            feedRice(2.0);
            showGiftToast(user, '甜甜圈', 2.0, '🍩');
          }
          currentActionTimeout = setTimeout(resetToIdle, 2700);
          break;

        // -------------------------------------------------------------
        // 10. 棒棒糖 (9抖币 · 核心王牌特技：3D 真实抱肚子狂笑 · 原声锁帧同步)
        // -------------------------------------------------------------
        case 'belly_laugh':
        case 'laugh':
        case 'gold':
          const stageEl = document.querySelector('.stage-container');
          if (stageEl) stageEl.classList.add('action-active');

          if (!fromGiftEvent) {
            feedRice(1.8);
            showGiftToast(user, '棒棒糖', 1.8, '🍭');
          }
          setSpeech(`哈哈哈哈！哎呀妈呀！【${user}】的棒棒糖太逗了！肚子笑抽筋啦！哈哈哈哈哈哈！`);

          const actionVideo = document.getElementById('video-action-player');
          const groundShadowBelly = document.getElementById('ground-shadow');
          const eq = document.getElementById('audio-equalizer');
          if (eq) eq.classList.add('active');

          if (groundShadowBelly) {
            groundShadowBelly.className = 'ground-shadow shadow-belly-laugh';
          }

          // 2D 待机体平滑淡出，随后隐藏防止透明背景穿模
          rig.style.transition = 'opacity 0.18s ease, transform 0.22s ease';
          rig.style.transform = 'scale(1.1) translateY(-10px)';
          setTimeout(() => {
            rig.style.opacity = '0';
            setTimeout(() => {
              if (actionVideo && actionVideo.classList.contains('active')) {
                rig.style.display = 'none';
              }
            }, 100);
          }, 80);

          // 唤醒并播放 3D 抱肚子大笑动作视频层 (原生内嵌音轨，零延迟音画同步)
          if (actionVideo) {
            actionVideo.volume = voiceVolume;
            actionVideo.currentTime = 0;
            actionVideo.classList.add('active');
            
            const playPromise = actionVideo.play();
            if (playPromise !== undefined) {
              playPromise.catch(err => {
                console.warn('Action video autoplay blocked, trying unmuted:', err);
                actionVideo.muted = false;
                actionVideo.play();
              });
            }
          }

          // 伴随狂笑节奏爆发震屏与爆笑粒子特效
          triggerScreenShake();
          spawnGPUParticles('🤣', 28);
          spawnGPUParticles('✨', 20);

          let laughTimer1 = setTimeout(() => {
            triggerScreenShake();
            spawnGPUParticles('🤣', 22);
            spawnGPUParticles('💥', 15);
          }, 3500);

          let laughTimer2 = setTimeout(() => {
            triggerScreenShake();
            spawnGPUParticles('🤣', 25);
            spawnGPUParticles('✨', 20);
          }, 7000);

          // 9.1s 完整大笑结束后，亲口深情答谢送礼观众并平滑还原待机状态
          currentActionTimeout = setTimeout(() => {
            clearTimeout(laughTimer1);
            clearTimeout(laughTimer2);
            playNaiwaAudio(ACTION_VOICES.bloat, `呼……笑得我肚皮好酸呀～谢谢【${user}】送的甜蜜棒棒糖，奶娃开心到飞起啦！`);
            resetToIdle();
          }, 9200);
          break;

        // -------------------------------------------------------------
        // 免费指令与辅助交互
        // -------------------------------------------------------------
        case 'bubbles': // 吐泡泡
          playNaiwaAudio(ACTION_VOICES.bubbles, '咕噜噜～奶娃吐了好多好玩的大泡泡！', true);
          rig.className = 'character-rig idle-breath';
          setEyes('happy');
          setMouth('o');
          spawnBubbles(35);
          currentActionTimeout = setTimeout(resetToIdle, 2500);
          break;

        case 'sleep': // 睡觉呼呼
          playNaiwaAudio(ACTION_VOICES.sleep, '呼噜噜……好困呀，让奶娃眯一小会儿……', true);
          rig.className = 'character-rig idle-breath';
          setEyes('happy');
          setMouth('neutral');
          sleepBubble.classList.add('active');
          currentActionTimeout = setTimeout(resetToIdle, 3800);
          break;

        case 'squish': // 恶搞压扁
          spawnHammerEffect();
          setTimeout(() => {
            triggerScreenShake();
            rig.className = 'character-rig anim-squish';
            setEyes('dizzy');
            setMouth('wavy');
            playNaiwaAudio(ACTION_VOICES.squish, '哎哟！好疼！谁把奶娃压扁扁啦！', true);
            spawnGPUParticles('💥', 25);
          }, 450);
          currentActionTimeout = setTimeout(resetToIdle, 2800);
          break;

        case 'dance': // 摇摆跳舞
          playNaiwaAudio(ACTION_VOICES.dance, '耶，帅的代名词就是我耶！一起摇摆！', true);
          rig.className = 'character-rig anim-dance';
          setEyes('happy');
          setMouth('open');
          spawnGPUParticles('🎵', 28);
          currentActionTimeout = setTimeout(resetToIdle, 3000);
          break;
      }
    }
\n"""
content = content[:start_idx] + new_trigger_section + content[end_idx:]
print("7. Replaced triggerAction.")

# 8. 更新 handleGiftEvent 传递 user 参数并标明 fromGiftEvent = true
target_gift_call = """        } else {
          triggerAction(match.action);
        }
      } else {
        triggerAction('blush'); // 默认未知礼物害羞感谢
      }"""

replacement_gift_call = """        } else {
          triggerAction(match.action, user, true);
        }
      } else {
        triggerAction('blush', user, true); // 默认未知礼物害羞感谢
      }"""

assert target_gift_call in content, "target_gift_call not found"
content = content.replace(target_gift_call, replacement_gift_call)
print("8. Updated handleGiftEvent triggerAction call.")

# 9. 在 handleSongRequest VIP 分支中增加 playSFX('assets/sfx/crown_shimmer.wav') 与 setAtmosphere('gold-vip-mode', 2800)
target_vip_song_action = """        // 视听大动效反馈：星光升空漂浮 + 音符金光粒子爆发 + 亲口语音欢呼感谢
        playNaiwaAudio(ACTION_VOICES.song, `哇！收到【为你点亮】啦！感谢${userName}开启VIP专属通道，已立刻插队播放《${cleanName}》～`, true);"""

replacement_vip_song_action = """        // 视听大动效反馈：星光升空漂浮 + 音符金光粒子爆发 + 亲口语音欢呼感谢
        playSFX('assets/sfx/crown_shimmer.wav');
        setAtmosphere('gold-vip-mode', 2800);
        playNaiwaAudio(ACTION_VOICES.song, `哇！收到【为你点亮】啦！感谢${userName}开启VIP专属通道，已立刻插队播放《${cleanName}》～`, true);"""

assert target_vip_song_action in content, "target_vip_song_action not found"
content = content.replace(target_vip_song_action, replacement_vip_song_action)
print("9. Added playSFX & setAtmosphere to handleSongRequest VIP branch.")

# 写入文件，明确使用 newline='\n' 防止 Windows 行尾膨胀
with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Update completed successfully! Line count:", len(content.splitlines()))
