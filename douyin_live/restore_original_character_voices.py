# -*- coding: utf-8 -*-
import os

html_path = 'D:/zhibo/Open-LLM-VTuber/douyin_live/index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('\r\n', '\n')

# 1. 定义顶部的 ACTION_VOICES
top_action_voices = """    // 100% 官方原版奶龙原声音频切片 (用户最喜欢的纯正奶龙/小黄人原声)
    const ACTION_VOICES = {
      intro: 'assets/voice/intro.mp3',       // “我是奶龙！”
      boing: 'assets/voice/boing.mp3',       // “耶，帅的代名词就是我耶，胜利了！”
      bubbles: 'assets/voice/bubbles.mp3',   // “胜利了！”
      sleep: 'assets/voice/sleep.mp3',       // “求求你了，我想要好多好吃的！”
      squish: 'assets/voice/squish.mp3',     // “哼，你们给我等着！”
      bloat: 'assets/voice/bloat.mp3',       // “我的大肚肚真的很酷酷！”
      blush: 'assets/voice/blush.mp3',       // “哼，小熊！”
      dance: 'assets/voice/dance.mp3',       // “耶，帅的代名词就是我耶！”
      shiver: 'assets/voice/shiver.mp3',     // “你以为我会怕你吗？我根本不害怕的！”
      hearts: 'assets/voice/hearts.mp3',     // “耶，帅的代名词就是我耶，胜利了！”
      gold: 'assets/voice/gold.mp3',         // “奶龙魔性八级狂笑 (哈哈哈哈哈哈)”
      hungry: 'assets/voice/hungry.mp3',     // “求求你了，我想要好多好吃的！”
      revive: 'assets/voice/revive.mp3',     // “我的大肚肚真的很酷酷！”
      song: 'assets/voice/song.mp3'          // “耶，帅的代名词就是我耶！”
    };
"""

# 在 RIG_ASSETS 后面直接插入顶置的 ACTION_VOICES
target_rig_assets_end = """      mouth: {
        neutral: 'assets/rig/mouth_neutral.png',
        open: 'assets/rig/mouth_open.png',
        o: 'assets/rig/mouth_o.png',
        wavy: 'assets/rig/mouth_wavy.png'
      }
    };"""

assert target_rig_assets_end in content, "target_rig_assets_end not found"
content = content.replace(target_rig_assets_end, target_rig_assets_end + "\n\n" + top_action_voices)
print("1. Elevated ACTION_VOICES to the top of script.")

# 移除原有位置重复的 const ACTION_VOICES
old_action_voices_block = """    // 100% 官方原版奶龙原声切片映射表 (无任何AI假声/机械音)
    const ACTION_VOICES = {
      intro: 'assets/voice/intro.mp3',       // “我是奶龙！”
      boing: 'assets/voice/boing.mp3',       // “耶，帅的代名词就是我耶，胜利了！”
      bubbles: 'assets/voice/bubbles.mp3',   // “胜利了！”
      sleep: 'assets/voice/sleep.mp3',       // “求求你了，我想要好多好吃的！”
      squish: 'assets/voice/squish.mp3',     // “哼，你们给我等着！”
      bloat: 'assets/voice/bloat.mp3',       // “我的大肚肚真的很酷酷！”
      blush: 'assets/voice/blush.mp3',       // “哼，小熊！”
      dance: 'assets/voice/dance.mp3',       // “耶，帅的代名词就是我耶！”
      shiver: 'assets/voice/shiver.mp3',     // “你以为我会怕你吗？我根本不害怕的！”
      hearts: 'assets/voice/hearts.mp3',     // “耶，帅的代名词就是我耶，胜利了！”
      gold: 'assets/voice/gold.mp3',         // “奶龙魔性八级狂笑 (哈哈哈哈哈哈)”
      hungry: 'assets/voice/hungry.mp3',     // “求求你了，我想要好多好吃的！”
      revive: 'assets/voice/revive.mp3',     // “我的大肚肚真的很酷酷！”
      song: 'assets/voice/song.mp3'          // “耶，帅的代名词就是我耶！”
    };"""

if old_action_voices_block in content:
    content = content.replace(old_action_voices_block, "// (ACTION_VOICES 已统一提升至顶部全局)")
    print("2. Removed duplicate ACTION_VOICES definition.")

# 2. 全面更新 triggerAction: 10款礼物全部使用原版音频切片，且每一款礼物音频完全不同！
start_idx = content.find("    // 动作与特效触发调度 (全面升级：10大官方礼物专属定制心意、拟声音效、专属动作道具与独一无二台词)")
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
        // 1. 小心心 (1抖币 · 原汁原味傲娇害羞原声 · 3D搏动心跳道具 · 砰砰心跳声)
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
          playNaiwaAudio(ACTION_VOICES.blush, `哇！谢谢【${user}】送的小心心，奶娃心里扑通扑通跳个不停呢！`, true);
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
        // 2. 抖音 (1抖币 · 原汁原味胜利活力原声 · DJ耳机跳动音符道具 · 欢快礼花声)
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
          playNaiwaAudio(ACTION_VOICES.boing, `收到【${user}】的抖音专属音符！动次打次，跟着奶娃一起摇摆起来吧！`, true);
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
        // 3. 玫瑰 (1抖币 · 原汁原味浪漫天籁原声 · 99朵红玫瑰捧花与飞吻道具 · 啵唧飞吻声)
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
          playNaiwaAudio(ACTION_VOICES.song, `哇！好香的红玫瑰！啵唧，送给【${user}】一个超级甜蜜的飞吻哦！`, true);
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
        // 4. 人气票 (1抖币 · 原汁原味欢呼胜利原声 · 应援荧光棒与TOP1金牌道具 · 礼炮声)
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
          playNaiwaAudio(ACTION_VOICES.bubbles, `人气暴涨啦！感谢【${user}】投出的人气票，奶娃冲鸭冲榜一！`, true);
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
        // 5. 大啤酒 (2抖币 · 原汁原味酷酷大肚肚原声 · 倾倒扎啤倒酒与BURP大饱嗝道具 · 倒酒饱嗝声)
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
          playNaiwaAudio(ACTION_VOICES.bloat, `哈，好爽快的大啤酒！吨吨吨，嗝，谢谢【${user}】大哥喝饱饱啦！`, true);
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
        // 6. 你最好看 (2抖币 · 原汁原味超帅帅气原声 · 单反快门爆闪与颜值100分道具 · 双粉心瞳孔)
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
          playNaiwaAudio(ACTION_VOICES.dance, `眼里全是你！【${user}】在奶娃心里就是全宇宙最好看最帅气的小可爱！`, true);
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
        // 7. 手势比心 (5抖币 · 原汁原味超能爱心原声 · 双指尖比心与激光光波道具 · 激光轰鸣声)
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
          playNaiwaAudio(ACTION_VOICES.hearts, `收到超级大爱心！超能爱心光波，发射！【${user}】一定要接住满满的幸福哦！`, true);
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
        // 8. 为你点亮 (9抖币 · 原汁原味满血复活尊贵原声 · 璀璨皇冠降临加冕与VIP横幅 · 天使竖琴声)
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
          playNaiwaAudio(ACTION_VOICES.revive, `璀璨星光为你点亮！感谢【${user}】开启VIP通道，快快发歌名插队吧！`, true);
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
        // 9. 甜甜圈 (10抖币 · 原汁原味贪吃想吃原声 · 飞入大甜甜圈与嗷呜咬痕道具 · 肚皮膨胀回弹)
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
          playNaiwaAudio(ACTION_VOICES.hungry, `嗷呜！好甜好香的甜甜圈！【${user}】喂饱饱啦，肚皮变得圆滚滚像个大皮球啦！`, true);
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
        // 10. 棒棒糖 (9抖币 · 3D视频真实抱肚子狂笑锁帧原声 · 结束后亲切答谢)
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

          // 9.1s 完整大笑结束后，用官方原声答谢送礼观众并平滑还原待机状态
          currentActionTimeout = setTimeout(() => {
            clearTimeout(laughTimer1);
            clearTimeout(laughTimer2);
            playNaiwaAudio(ACTION_VOICES.intro, `呼……笑得我肚皮好酸呀～谢谢【${user}】送的甜蜜棒棒糖，奶娃开心到飞起啦！`);
            resetToIdle();
          }, 9200);
          break;

        // -------------------------------------------------------------
        // 免费指令与辅助交互 (保持原版原声)
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
print("3. Replaced triggerAction with 100% original authentic character voices.")

# 4. handleSongRequest VIP 分支也使用 ACTION_VOICES.revive
target_vip_song = "playNaiwaAudio('assets/voice/gifts/gift_vip.mp3', `哇！收到【为你点亮】啦！"
replacement_vip_song = "playNaiwaAudio(ACTION_VOICES.revive, `哇！收到【为你点亮】啦！"
if target_vip_song in content:
    content = content.replace(target_vip_song, replacement_vip_song)
    print("4. Updated VIP song to ACTION_VOICES.revive.")

target_vip_danmaku = "playNaiwaAudio('assets/voice/gifts/gift_vip.mp3', `哇！感谢【${user}】送出【为你点亮】！"
replacement_vip_danmaku = "playNaiwaAudio(ACTION_VOICES.revive, `哇！感谢【${user}】送出【为你点亮】！"
if target_vip_danmaku in content:
    content = content.replace(target_vip_danmaku, replacement_vip_danmaku)

target_vip_custom = "playNaiwaAudio('assets/voice/gifts/gift_vip.mp3', `收到【${user}】的VIP指定歌单！"
replacement_vip_custom = "playNaiwaAudio(ACTION_VOICES.revive, `收到【${user}】的VIP指定歌单！"
if target_vip_custom in content:
    content = content.replace(target_vip_custom, replacement_vip_custom)

with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Update completed successfully! Line count:", len(content.splitlines()))
