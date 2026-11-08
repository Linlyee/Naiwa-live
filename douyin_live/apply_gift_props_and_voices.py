# -*- coding: utf-8 -*-
import os
import shutil

html_path = 'D:/zhibo/Open-LLM-VTuber/douyin_live/index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 统一 \n
content = content.replace('\r\n', '\n')

# -------------------------------------------------------------
# 1. 插入 Action Props 专属 CSS
# -------------------------------------------------------------
props_css = """
    /* ============ 动态专属道具层 (10大礼物真实可视道具动作) ============ */
    .action-props {
      position: absolute;
      bottom: 35px;
      left: 50%;
      transform: translateX(-50%);
      width: 530px;
      height: 710px;
      pointer-events: none;
      z-index: 15;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    /* 1. 小心心专属：巨型3D搏动爱心 */
    .prop-heart-beat {
      position: absolute;
      top: 42%;
      left: 50%;
      transform: translate(-50%, -50%);
      display: flex;
      flex-direction: column;
      align-items: center;
      animation: heartBeatingPop 1.8s ease-in-out infinite;
    }
    .giant-heart-glow {
      font-size: 110px;
      filter: drop-shadow(0 0 25px rgba(255, 60, 120, 0.95)) drop-shadow(0 0 50px rgba(255, 105, 180, 0.8));
      animation: heartScalePump 0.65s ease-in-out infinite alternate;
    }
    @keyframes heartScalePump {
      0% { transform: scale(0.9); }
      100% { transform: scale(1.28); }
    }
    .heart-caption {
      margin-top: 10px;
      background: linear-gradient(135deg, #ff2d55, #ff6b81);
      color: #fff;
      padding: 6px 18px;
      border-radius: 20px;
      font-size: 22px;
      font-weight: 800;
      box-shadow: 0 4px 15px rgba(255, 45, 85, 0.6);
      border: 2px solid #fff;
      animation: popBadge 0.4s cubic-bezier(0.18, 0.89, 0.32, 1.28);
    }

    /* 2. 抖音专属：DJ耳机与跳动双音符 */
    .prop-douyin {
      position: absolute;
      top: 18%;
      left: 50%;
      transform: translateX(-50%);
      width: 460px;
      height: 380px;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .prop-headphones {
      position: absolute;
      top: 10px;
      font-size: 130px;
      filter: drop-shadow(0 0 25px #00f2fe) drop-shadow(0 0 35px #4facfe);
      animation: headphoneBounce 0.6s ease-in-out infinite alternate;
    }
    @keyframes headphoneBounce {
      0% { transform: translateY(0) scale(1); }
      100% { transform: translateY(-15px) scale(1.08); }
    }
    .bounce-note {
      position: absolute;
      font-size: 75px;
      filter: drop-shadow(0 0 15px #ffd043);
    }
    .note-left {
      left: 15px;
      top: 70px;
      animation: noteFloatL 1.2s ease-in-out infinite alternate;
    }
    .note-right {
      right: 15px;
      top: 80px;
      animation: noteFloatR 1.2s ease-in-out infinite alternate;
    }
    @keyframes noteFloatL {
      0% { transform: translateY(0) rotate(-15deg); }
      100% { transform: translateY(-35px) rotate(10deg); }
    }
    @keyframes noteFloatR {
      0% { transform: translateY(0) rotate(15deg); }
      100% { transform: translateY(-35px) rotate(-10deg); }
    }

    /* 3. 玫瑰专属：99朵抱怀红玫瑰与甜蜜飞吻唇印 */
    .prop-rose {
      position: absolute;
      bottom: 120px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .prop-bouquet {
      font-size: 135px;
      filter: drop-shadow(0 10px 25px rgba(255, 0, 80, 0.6));
      animation: bouquetSway 1.5s ease-in-out infinite alternate;
    }
    @keyframes bouquetSway {
      0% { transform: rotate(-5deg) scale(0.96); }
      100% { transform: rotate(5deg) scale(1.06); }
    }
    .prop-kiss-fly {
      position: absolute;
      top: -120px;
      font-size: 85px;
      filter: drop-shadow(0 0 20px #ff2d55);
      animation: kissFloatOut 1.8s ease-out infinite;
    }
    @keyframes kissFloatOut {
      0% { transform: scale(0.4) translateY(20px); opacity: 0; }
      35% { transform: scale(1.3) translateY(-30px); opacity: 1; }
      100% { transform: scale(1.8) translateY(-110px); opacity: 0; }
    }
    .rose-caption {
      margin-top: -15px;
      background: linear-gradient(135deg, #e91e63, #ff4081);
      color: #fff;
      padding: 6px 18px;
      border-radius: 20px;
      font-size: 22px;
      font-weight: 800;
      border: 2px solid #fff;
      box-shadow: 0 4px 15px rgba(233, 30, 99, 0.6);
    }

    /* 4. 人气票专属：应援双荧光棒与人气TOP1金牌 */
    .prop-cheer {
      position: absolute;
      top: 30%;
      left: 50%;
      transform: translateX(-50%);
      width: 500px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .lightstick {
      position: absolute;
      font-size: 85px;
      filter: drop-shadow(0 0 20px #ffd043);
    }
    .stick-l {
      left: 10px;
      animation: stickWaveL 0.5s ease-in-out infinite alternate;
    }
    .stick-r {
      right: 10px;
      animation: stickWaveR 0.5s ease-in-out infinite alternate;
    }
    @keyframes stickWaveL {
      0% { transform: rotate(-35deg) translateY(0); }
      100% { transform: rotate(10deg) translateY(-25px); }
    }
    @keyframes stickWaveR {
      0% { transform: rotate(35deg) translateY(0); }
      100% { transform: rotate(-10deg) translateY(-25px); }
    }
    .cheer-badge {
      margin-top: 15px;
      background: linear-gradient(135deg, #ff9800, #ff5722);
      color: #fff;
      padding: 8px 24px;
      border-radius: 24px;
      font-size: 24px;
      font-weight: 900;
      border: 2px solid #ffd043;
      box-shadow: 0 6px 20px rgba(255, 152, 0, 0.6);
      animation: cheerBadgeBounce 0.7s infinite alternate;
    }
    @keyframes cheerBadgeBounce {
      0% { transform: scale(0.95); }
      100% { transform: scale(1.08); }
    }

    /* 5. 大啤酒专属：倾倒倒酒大扎啤杯与爆笑打嗝气泡 */
    .prop-beer {
      position: absolute;
      bottom: 240px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .beer-glass-container {
      position: relative;
      animation: beerTiltChug 1.4s ease-in-out infinite alternate;
    }
    .beer-glass {
      font-size: 130px;
      filter: drop-shadow(0 10px 25px rgba(255, 180, 0, 0.7));
    }
    @keyframes beerTiltChug {
      0% { transform: rotate(0deg) scale(0.95); }
      50% { transform: rotate(-38deg) translateY(-18px) scale(1.15); }
      100% { transform: rotate(-48deg) translateY(-25px) scale(1.22); }
    }
    .burp-comic-badge {
      position: absolute;
      top: -110px;
      background: linear-gradient(135deg, #ffb300, #ff8f00);
      color: #fff;
      padding: 8px 26px;
      border-radius: 25px;
      font-size: 26px;
      font-weight: 900;
      border: 3px solid #fff;
      box-shadow: 0 6px 25px rgba(255, 179, 0, 0.8);
      animation: burpPop 0.8s cubic-bezier(0.18, 0.89, 0.32, 1.28) infinite alternate;
    }
    @keyframes burpPop {
      0% { transform: scale(0.92) rotate(-4deg); }
      100% { transform: scale(1.12) rotate(4deg); }
    }

    /* 6. 你最好看专属：单反闪光与100分颜值爆表横幅 */
    .prop-haokan {
      position: absolute;
      top: 35%;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .camera-flash-fx {
      font-size: 110px;
      filter: drop-shadow(0 0 35px #fff) drop-shadow(0 0 65px #ff69b4);
      animation: flashBlink 0.5s ease-in-out infinite alternate;
    }
    @keyframes flashBlink {
      0% { transform: scale(0.9); opacity: 0.8; }
      100% { transform: scale(1.25); opacity: 1; }
    }
    .beauty-banner {
      margin-top: 20px;
      background: linear-gradient(135deg, #ff4081, #e040fb);
      color: #fff;
      padding: 8px 24px;
      border-radius: 25px;
      font-size: 24px;
      font-weight: 900;
      border: 2px solid #fff;
      box-shadow: 0 6px 25px rgba(224, 64, 251, 0.6);
      animation: popBadge 0.4s ease-out;
    }

    /* 7. 手势比心专属：双指尖比心与超能激光爱心光波 */
    .prop-heart-beam {
      position: absolute;
      top: 40%;
      left: 50%;
      transform: translateX(-50%);
      width: 500px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .finger-hearts {
      font-size: 105px;
      filter: drop-shadow(0 0 30px #ff2d55);
      animation: fingerPulse 0.45s ease-in-out infinite alternate;
    }
    @keyframes fingerPulse {
      0% { transform: scale(0.92); }
      100% { transform: scale(1.18); }
    }
    .beam-caption {
      margin-top: 15px;
      background: linear-gradient(135deg, #ff1744, #ff5252);
      color: #fff;
      padding: 8px 26px;
      border-radius: 25px;
      font-size: 24px;
      font-weight: 900;
      border: 2px solid #fff;
      box-shadow: 0 0 30px rgba(255, 23, 68, 0.8);
      animation: beamWave 0.6s infinite alternate;
    }
    @keyframes beamWave {
      0% { transform: scale(0.95); box-shadow: 0 0 15px rgba(255,23,68,0.5); }
      100% { transform: scale(1.12); box-shadow: 0 0 40px rgba(255,23,68,1); }
    }

    /* 8. 为你点亮专属：头顶悬浮璀璨皇冠与金色VIP横幅 */
    .prop-vip-crown {
      position: absolute;
      top: -20px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .royal-crown {
      font-size: 125px;
      filter: drop-shadow(0 0 25px #ffd700) drop-shadow(0 0 45px #ffaa00);
      animation: crownFloatDescend 1.2s ease-in-out infinite alternate;
    }
    @keyframes crownFloatDescend {
      0% { transform: translateY(-15px) scale(0.94); }
      100% { transform: translateY(10px) scale(1.08); }
    }
    .vip-banner-gold {
      margin-top: 15px;
      background: linear-gradient(135deg, #ffb300, #ff8f00);
      color: #fff;
      padding: 8px 24px;
      border-radius: 25px;
      font-size: 22px;
      font-weight: 900;
      border: 2px solid #ffe082;
      box-shadow: 0 6px 30px rgba(255, 179, 0, 0.8);
      white-space: nowrap;
    }

    /* 9. 甜甜圈专属：大口嗷呜咬飞入甜甜圈与咬痕贴纸 */
    .prop-donut {
      position: absolute;
      top: 36%;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .flying-donut {
      font-size: 125px;
      filter: drop-shadow(0 10px 25px rgba(120, 60, 20, 0.6));
      animation: donutChompFly 1.2s ease-in-out infinite alternate;
    }
    @keyframes donutChompFly {
      0% { transform: translateY(15px) scale(0.9); }
      100% { transform: translateY(-15px) scale(1.22); }
    }
    .chomp-sticker {
      margin-top: 10px;
      background: linear-gradient(135deg, #8d6e63, #d84315);
      color: #fff;
      padding: 8px 24px;
      border-radius: 25px;
      font-size: 24px;
      font-weight: 900;
      border: 2px solid #ffe0b2;
      box-shadow: 0 6px 20px rgba(216, 67, 21, 0.6);
      animation: popBadge 0.4s ease-out;
    }

    @keyframes popBadge {
      0% { transform: scale(0.4); opacity: 0; }
      100% { transform: scale(1); opacity: 1; }
    }
"""

target_css_insert = "  </style>"
assert target_css_insert in content, "target_css_insert not found"
content = content.replace(target_css_insert, props_css + "\n  </style>")
print("1. Added Action Props CSS.")

# -------------------------------------------------------------
# 2. 在舞台中插入 action-props 容器
# -------------------------------------------------------------
target_stage_rig = """        <!-- 害羞红晕层 -->
        <img id="layer-blush" class="rig-layer" src="assets/blush.png" alt="Blush">
      </div>

      <!-- 睡觉浮动气泡 -->"""

replacement_stage_rig = """        <!-- 害羞红晕层 -->
        <img id="layer-blush" class="rig-layer" src="assets/blush.png" alt="Blush">
      </div>

      <!-- 动态专属动作道具层 -->
      <div id="action-props" class="action-props"></div>

      <!-- 睡觉浮动气泡 -->"""

assert target_stage_rig in content, "target_stage_rig not found"
content = content.replace(target_stage_rig, replacement_stage_rig)
print("2. Added action-props container into stage.")

# -------------------------------------------------------------
# 3. 在 resetToIdle 中清理 action-props
# -------------------------------------------------------------
target_clean_idle = """      sleepBubble.classList.remove('active');
      if (atmosphereOverlay) atmosphereOverlay.className = 'atmosphere-overlay';"""

replacement_clean_idle = """      sleepBubble.classList.remove('active');
      const actionPropsEl = document.getElementById('action-props');
      if (actionPropsEl) actionPropsEl.innerHTML = '';
      if (atmosphereOverlay) atmosphereOverlay.className = 'atmosphere-overlay';"""

assert target_clean_idle in content, "target_clean_idle not found"
content = content.replace(target_clean_idle, replacement_clean_idle)
print("3. Added action-props cleanup to resetToIdle.")

# -------------------------------------------------------------
# 4. 全面重构 triggerAction:
# 每个礼物专属语音文件 (gift_xxx.mp3) + 专属台词 + 专属道具视觉 + 专属动作 + 专属音效
# -------------------------------------------------------------
start_idx = content.find("    // 动作与特效触发调度 (全面升级：10大官方礼物专属定制心意、拟声音效、专属动作与全屏氛围)")
end_idx = content.find("    // =======================================================\n    // 奶娃真实高保真语音驱动引擎")
assert start_idx != -1 and end_idx != -1, "triggerAction boundaries not found"

new_trigger = """    // 动作与特效触发调度 (全面升级：10大官方礼物专属定制心意、拟声音效、专属动作道具与独一无二台词)
    function triggerAction(action, user = '热心老铁', fromGiftEvent = false) {
      if (isTalking) stopTalking();
      if (currentActionTimeout) clearTimeout(currentActionTimeout);
      if (sleepBubble) sleepBubble.classList.remove('active');
      if (atmosphereOverlay) atmosphereOverlay.className = 'atmosphere-overlay';

      const actionPropsEl = document.getElementById('action-props');
      if (actionPropsEl) actionPropsEl.innerHTML = '';

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
        // 1. 小心心 (1抖币 · 专属动作：胸口巨大爱心搏动 · 专属台词 · 心跳拟声音效)
        // -------------------------------------------------------------
        case 'blush':
          playSFX('assets/sfx/heartbeat.wav');
          if (actionPropsEl) {
            actionPropsEl.innerHTML = `
              <div class="prop-heart-beat">
                <div class="giant-heart-glow">💖</div>
                <div class="heart-caption">心跳小鹿乱撞 💓</div>
              </div>
            `;
          }
          playNaiwaAudio('assets/voice/gifts/gift_blush.mp3', `哇！谢谢【${user}】送的小心心，奶娃心里扑通扑通跳个不停呢！`, true);
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
          currentActionTimeout = setTimeout(resetToIdle, 2800);
          break;

        // -------------------------------------------------------------
        // 2. 抖音 (1抖币 · 专属动作：DJ耳机与跳动双音符 · 专属台词 · 欢快礼花声)
        // -------------------------------------------------------------
        case 'boing':
          playSFX('assets/sfx/confetti.wav');
          if (actionPropsEl) {
            actionPropsEl.innerHTML = `
              <div class="prop-douyin">
                <div class="prop-headphones">🎧</div>
                <div class="bounce-note note-left">🎵</div>
                <div class="bounce-note note-right">🎶</div>
              </div>
            `;
          }
          playNaiwaAudio('assets/voice/gifts/gift_boing.mp3', `收到【${user}】的抖音专属音符！动次打次，跟着奶娃一起摇摆起来吧！`, true);
          rig.className = 'character-rig anim-boing';
          setEyes('happy');
          setMouth('open');
          spawnGPUParticles('🎵', 30);
          spawnGPUParticles('✨', 25);
          if (!fromGiftEvent) {
            feedRice(0.2);
            showGiftToast(user, '抖音', 0.2, '🎵');
          }
          currentActionTimeout = setTimeout(resetToIdle, 2400);
          break;

        // -------------------------------------------------------------
        // 3. 玫瑰 (1抖币 · 专属动作：99朵玫瑰手捧花与甜蜜飞吻 · 专属台词 · 啵唧飞吻声)
        // -------------------------------------------------------------
        case 'rose':
          playSFX('assets/sfx/kiss.wav');
          if (actionPropsEl) {
            actionPropsEl.innerHTML = `
              <div class="prop-rose">
                <div class="prop-bouquet">💐🌹</div>
                <div class="prop-kiss-fly">💋</div>
                <div class="rose-caption">深情飞吻 99朵玫瑰 🌹</div>
              </div>
            `;
          }
          playNaiwaAudio('assets/voice/gifts/gift_rose.mp3', `哇！好香的红玫瑰！啵唧，送给【${user}】一个超级甜蜜的飞吻哦！`, true);
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
          currentActionTimeout = setTimeout(resetToIdle, 2800);
          break;

        // -------------------------------------------------------------
        // 4. 人气票 (1抖币 · 专属动作：应援双荧光棒挥舞与人气TOP1金牌 · 专属台词 · 礼炮声)
        // -------------------------------------------------------------
        case 'praise':
          playSFX('assets/sfx/confetti.wav');
          if (actionPropsEl) {
            actionPropsEl.innerHTML = `
              <div class="prop-cheer">
                <div class="lightstick stick-l">✨🪄</div>
                <div class="lightstick stick-r">🪄✨</div>
                <div class="cheer-badge">🏆 人气王 TOP 1 🏆</div>
              </div>
            `;
          }
          playNaiwaAudio('assets/voice/gifts/gift_praise.mp3', `人气暴涨啦！感谢【${user}】投出的人气票，奶娃冲鸭冲榜一！`, true);
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
          currentActionTimeout = setTimeout(resetToIdle, 2500);
          break;

        // -------------------------------------------------------------
        // 5. 大啤酒 (2抖币 · 专属动作：倾倒大扎啤杯倒酒与爆笑打嗝气泡 · 专属台词 · 咕嘟打饱嗝声)
        // -------------------------------------------------------------
        case 'pijiu':
          playSFX('assets/sfx/beer_chug.wav');
          if (actionPropsEl) {
            actionPropsEl.innerHTML = `
              <div class="prop-beer">
                <div class="beer-glass-container">
                  <div class="beer-glass">🍺</div>
                </div>
                <div class="burp-comic-badge">BURP! 嗝~~~ 🍺</div>
              </div>
            `;
          }
          playNaiwaAudio('assets/voice/gifts/gift_pijiu.mp3', `哈，好爽快的大啤酒！吨吨吨，嗝，谢谢【${user}】大哥喝饱饱啦！`, true);
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
          currentActionTimeout = setTimeout(resetToIdle, 3000);
          break;

        // -------------------------------------------------------------
        // 6. 你最好看 (2抖币 · 专属动作：单反闪光灯与100分颜值爆表横幅 · 双粉心瞳孔 · 专属台词)
        // -------------------------------------------------------------
        case 'haokan':
          playSFX('assets/sfx/sparkle_camera.wav');
          if (actionPropsEl) {
            actionPropsEl.innerHTML = `
              <div class="prop-haokan">
                <div class="camera-flash-fx">📸</div>
                <div class="beauty-banner">✨ 颜值爆表 100分 ✨</div>
              </div>
            `;
          }
          playNaiwaAudio('assets/voice/gifts/gift_haokan.mp3', `眼里全是你！【${user}】在奶娃心里就是全宇宙最好看最帅气的小可爱！`, true);
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
          currentActionTimeout = setTimeout(resetToIdle, 2800);
          break;

        // -------------------------------------------------------------
        // 7. 手势比心 (5抖币 · 专属动作：双指尖比心与超能激光爱心光波 · 专属台词 · 激光轰鸣声)
        // -------------------------------------------------------------
        case 'hearts':
          playSFX('assets/sfx/heart_beam.wav');
          if (actionPropsEl) {
            actionPropsEl.innerHTML = `
              <div class="prop-heart-beam">
                <div class="finger-hearts">🫰💖🫰</div>
                <div class="beam-caption">超能爱心光波！BIU~ ⚡</div>
              </div>
            `;
          }
          playNaiwaAudio('assets/voice/gifts/gift_hearts.mp3', `收到超级大爱心！超能爱心光波，发射！【${user}】一定要接住满满的幸福哦！`, true);
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
          currentActionTimeout = setTimeout(resetToIdle, 3000);
          break;

        // -------------------------------------------------------------
        // 8. 为你点亮 (9抖币 · 专属动作：璀璨皇冠降临加冕与金色VIP横幅 · 专属台词 · 天使竖琴声)
        // -------------------------------------------------------------
        case 'vip_song':
        case 'balloon':
          playSFX('assets/sfx/crown_shimmer.wav');
          if (actionPropsEl) {
            actionPropsEl.innerHTML = `
              <div class="prop-vip-crown">
                <div class="royal-crown">👑</div>
                <div class="vip-banner-gold">👑 VIP霸权插队点歌已激活 👑</div>
              </div>
            `;
          }
          playNaiwaAudio('assets/voice/gifts/gift_vip.mp3', `璀璨星光为你点亮！感谢【${user}】开启VIP通道，快快发歌名插队吧！`, true);
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
          currentActionTimeout = setTimeout(resetToIdle, 3000);
          break;

        // -------------------------------------------------------------
        // 9. 甜甜圈 (10抖币 · 专属动作：大口嗷呜咬飞入甜甜圈与咬痕贴纸 · 肚皮膨胀 · 专属台词)
        // -------------------------------------------------------------
        case 'donut':
          playSFX('assets/sfx/donut_eat.wav');
          if (actionPropsEl) {
            actionPropsEl.innerHTML = `
              <div class="prop-donut">
                <div class="flying-donut">🍩</div>
                <div class="chomp-sticker">CHOMP! 嗷呜大口吃~ 🍩</div>
              </div>
            `;
          }
          playNaiwaAudio('assets/voice/gifts/gift_donut.mp3', `嗷呜！好甜好香的甜甜圈！【${user}】喂饱饱啦，肚皮变得圆滚滚像个大皮球啦！`, true);
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
          currentActionTimeout = setTimeout(resetToIdle, 3000);
          break;

        // -------------------------------------------------------------
        // 10. 棒棒糖 (9抖币 · 核心王牌特技：3D 真实抱肚子狂笑 · 原声锁帧同步 · 专属台词)
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
            playNaiwaAudio('assets/voice/gifts/gift_lollipop.mp3', `呼……笑得我肚皮好酸呀～谢谢【${user}】送的甜蜜棒棒糖，奶娃开心到飞起啦！`);
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

content = content[:start_idx] + new_trigger + content[end_idx:]
print("4. Replaced triggerAction with props and dedicated gift voices.")

with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Update completed successfully! Line count:", len(content.splitlines()))
