# -*- coding: utf-8 -*-
with open('douyin_live/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. 优化跑道宽度与尺寸，完美嵌入中央安全通道 (不触碰顶部口令条，不遮挡左右礼物标签)
old_toast_css = """    /* 大礼物专属横幅跑道 (Gift Toast Banner) */
    #gift-toast-container {
      position: absolute;
      top: 405px;
      left: 50%;
      transform: translateX(-50%);
      width: 860px;
      pointer-events: none;
      z-index: 55;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
    }

    .gift-toast {
      background: linear-gradient(135deg, rgba(255, 107, 139, 0.94), rgba(255, 184, 0, 0.96));
      border: 2px solid #ffffff;
      border-radius: 36px;
      padding: 12px 30px;
      display: flex;
      align-items: center;
      gap: 16px;
      box-shadow: 0 10px 30px rgba(255, 107, 139, 0.6), 0 0 25px rgba(255, 208, 67, 0.85);
      animation: toastPop 3.6s cubic-bezier(0.25, 1, 0.5, 1) forwards;
      transform-origin: center;
    }

    @keyframes toastPop {
      0% { transform: translateY(-30px) scale(0.85); opacity: 0; }
      14% { transform: translateY(0) scale(1.05); opacity: 1; }
      20% { transform: translateY(0) scale(1); opacity: 1; }
      85% { transform: translateY(0) scale(1); opacity: 1; }
      100% { transform: translateY(-40px) scale(0.9); opacity: 0; }
    }

    .toast-avatar { font-size: 34px; }
    .toast-text { font-size: 26px; font-weight: 800; color: #ffffff; text-shadow: 0 2px 6px rgba(0,0,0,0.45); }"""

new_toast_css = """    /* 大礼物专属横幅跑道 (Gift Toast Banner) · 黄金中央走廊设计 */
    #gift-toast-container {
      position: absolute;
      top: 418px;
      left: 50%;
      transform: translateX(-50%);
      width: auto;
      max-width: 530px;
      pointer-events: none;
      z-index: 55;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
    }

    .gift-toast {
      background: linear-gradient(135deg, rgba(255, 107, 139, 0.95), rgba(255, 184, 0, 0.96));
      border: 2px solid #ffffff;
      border-radius: 28px;
      padding: 8px 22px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 10px 25px rgba(255, 107, 139, 0.55), 0 0 20px rgba(255, 208, 67, 0.75);
      animation: toastPop 3.6s cubic-bezier(0.25, 1, 0.5, 1) forwards;
      transform-origin: center;
      white-space: nowrap;
    }

    @keyframes toastPop {
      0% { transform: translateY(-15px) scale(0.9); opacity: 0; }
      14% { transform: translateY(0) scale(1.03); opacity: 1; }
      20% { transform: translateY(0) scale(1); opacity: 1; }
      85% { transform: translateY(0) scale(1); opacity: 1; }
      100% { transform: translateY(-20px) scale(0.95); opacity: 0; }
    }

    .toast-avatar { font-size: 28px; }
    .toast-text { font-size: 21px; font-weight: 800; color: #ffffff; text-shadow: 0 2px 6px rgba(0,0,0,0.45); }"""

c = c.replace(old_toast_css, new_toast_css)

# 2. 导演台悬浮球微缩精炼，避免遮挡点歌台信息
old_fab = """.director-fab {
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: linear-gradient(135deg, #ffd043, #ff9000);
      color: #000;
      font-weight: 800;
      font-size: 20px;
      padding: 12px 24px;
      border-radius: 30px;
      box-shadow: 0 8px 25px rgba(255, 170, 0, 0.5);
      cursor: pointer;
      z-index: 999;
      border: none;
      transition: transform 0.2s;
    }"""

new_fab = """.director-fab {
      position: fixed;
      bottom: 8px;
      right: 12px;
      background: linear-gradient(135deg, #ffd043, #ff9000);
      color: #000;
      font-weight: 800;
      font-size: 15px;
      padding: 6px 16px;
      border-radius: 20px;
      box-shadow: 0 4px 15px rgba(255, 170, 0, 0.4);
      cursor: pointer;
      z-index: 999;
      border: none;
      opacity: 0.85;
      transition: transform 0.2s, opacity 0.2s;
    }
    .director-fab:hover { opacity: 1; }"""

c = c.replace(old_fab, new_fab)

with open('douyin_live/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Applied final UI precision polish!")
