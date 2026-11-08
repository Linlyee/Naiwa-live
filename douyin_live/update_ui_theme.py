import os

index_path = r'D:\zhibo\Open-LLM-VTuber\douyin_live\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update background to use live_bg.jpg
html = html.replace(
    'background: radial-gradient(circle at 50% 35%, #182c42 0%, #0d1a27 50%, #060c13 100%);',
    "background: url('assets/live_bg.jpg') center center / cover no-repeat, #0a1118;"
)

# 2. Add gift-icon-img CSS
gift_css = '''
    .action-icon-img {
      width: 48px;
      height: 48px;
      object-fit: contain;
      filter: drop-shadow(0 3px 6px rgba(0, 0, 0, 0.45));
    }
'''
if '.action-icon-img' not in html:
    html = html.replace('.action-icon {', gift_css + '\n    .action-icon {')

# 3. Replace left side action tags
old_left = '''    <!-- 3. 左侧动作指令列表 -->
    <div class="action-side side-left">
      <div class="action-tag" onclick="triggerAction('squish')">
        <span class="action-icon">💖</span>
        <span class="action-text">心动压扁</span>
      </div>
      <div class="action-tag" onclick="triggerAction('hearts')">
        <span class="action-icon">🍧</span>
        <span class="action-text">爱到埋住</span>
      </div>
      <div class="action-tag" onclick="triggerAction('dance')">
        <span class="action-icon">🚀</span>
        <span class="action-text">摇摆翻车</span>
      </div>
      <div class="action-tag" onclick="triggerAction('blush')">
        <span class="action-icon">🎆</span>
        <span class="action-text">害羞夸夸</span>
      </div>
      <div class="action-tag" onclick="triggerAction('squish')">
        <span class="action-icon">🥞</span>
        <span class="action-text">变荷包蛋</span>
      </div>
    </div>'''

new_left = '''    <!-- 3. 左侧动作指令列表 (真实抖音礼物图标) -->
    <div class="action-side side-left">
      <div class="action-tag" onclick="triggerAction('squish')">
        <img class="action-icon-img" src="assets/gifts/xindong.png" alt="心动压扁">
        <span class="action-text">心动压扁</span>
      </div>
      <div class="action-tag" onclick="triggerAction('hearts')">
        <img class="action-icon-img" src="assets/gifts/aidao.png" alt="爱到埋住">
        <span class="action-text">爱到埋住</span>
      </div>
      <div class="action-tag" onclick="triggerAction('dance')">
        <img class="action-icon-img" src="assets/gifts/kuangbiao.png" alt="狂飙翻车">
        <span class="action-text">狂飙翻车</span>
      </div>
      <div class="action-tag" onclick="triggerAction('blush')">
        <img class="action-icon-img" src="assets/gifts/jidong.png" alt="激动上头">
        <span class="action-text">激动上头</span>
      </div>
      <div class="action-tag" onclick="triggerAction('squish')">
        <img class="action-icon-img" src="assets/gifts/tiane.png" alt="天鹅变鸽">
        <span class="action-text">天鹅变鸽</span>
      </div>
    </div>'''

html = html.replace(old_left, new_left)

# 4. Replace right side action tags
old_right = '''    <!-- 4. 右侧动作指令列表 -->
    <div class="action-side side-right">
      <div class="action-tag" onclick="triggerAction('gold')">
        <span class="action-text">摘星暴击</span>
        <span class="action-icon">✨</span>
      </div>
      <div class="action-tag" onclick="triggerAction('boing')">
        <span class="action-text">果冻弹跳</span>
        <span class="action-icon">🐰</span>
      </div>
      <div class="action-tag" onclick="triggerAction('bloat')">
        <span class="action-text">贪吃过载</span>
        <span class="action-icon">🎃</span>
      </div>
      <div class="action-tag" onclick="triggerAction('shiver')">
        <span class="action-text">惊吓发抖</span>
        <span class="action-icon">🎁</span>
      </div>
      <div class="action-tag" onclick="triggerAction('bubbles')">
        <span class="action-text">气球炸场</span>
        <span class="action-icon">🎈</span>
      </div>
    </div>'''

new_right = '''    <!-- 4. 右侧动作指令列表 (真实抖音礼物图标) -->
    <div class="action-side side-right">
      <div class="action-tag" onclick="triggerAction('gold')">
        <span class="action-text">摘星暴击</span>
        <img class="action-icon-img" src="assets/gifts/zhaixing.png" alt="摘星暴击">
      </div>
      <div class="action-tag" onclick="triggerAction('boing')">
        <span class="action-text">爱心暴击</span>
        <img class="action-icon-img" src="assets/gifts/aixin.png" alt="爱心暴击">
      </div>
      <div class="action-tag" onclick="triggerAction('bloat')">
        <span class="action-text">贪吃过载</span>
        <img class="action-icon-img" src="assets/gifts/tanchi.png" alt="贪吃过载">
      </div>
      <div class="action-tag" onclick="triggerAction('shiver')">
        <span class="action-text">惊吓开箱</span>
        <img class="action-icon-img" src="assets/gifts/jingxia.png" alt="惊吓开箱">
      </div>
      <div class="action-tag" onclick="triggerAction('bubbles')">
        <span class="action-text">气球炸场</span>
        <img class="action-icon-img" src="assets/gifts/qiqiu.png" alt="气球炸场">
      </div>
    </div>'''

html = html.replace(old_right, new_right)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with genuine Douyin gift logos and dreamscape background!")
