import os
import numpy as np
from PIL import Image, ImageFilter

src = r'D:\zhibo\Open-LLM-VTuber\prompt\6af4258317383bba6b74287bf68843e6.jpg'
out_dir = r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\gifts'
os.makedirs(out_dir, exist_ok=True)

img = Image.open(src).convert('RGB')
arr = np.array(img, dtype=float)

# Coordinates on 6af... (size: 864 x 1920)
# Left 5:
# 1. 心动压扁: center y=555, x=56
# 2. 爱到埋住: center y=625, x=56
# 3. 狂飙翻车: center y=695, x=56
# 4. 激动上头: center y=765, x=56
# 5. 天鹅变鸽: center y=835, x=56
# Right 5:
# 1. 摘星暴击: center y=555, x=675
# 2. 爱心暴击: center y=625, x=675
# 3. 贪吃过载: center y=695, x=675
# 4. 惊吓开箱: center y=765, x=675
# 5. 气球炸场: center y=835, x=675

gifts = [
    ('xindong', 56, 555),
    ('aidao', 56, 625),
    ('kuangbiao', 56, 695),
    ('jidong', 56, 765),
    ('tiane', 56, 835),
    ('zhaixing', 675, 555),
    ('aixin', 675, 625),
    ('tanchi', 675, 695),
    ('jingxia', 675, 765),
    ('qiqiu', 675, 835),
]

r = 30 # radius 30 -> 60x60
bg_color = np.array([45.0, 65.0, 88.0])

for name, cx, cy in gifts:
    crop = arr[cy - r : cy + r, cx - r : cx + r, :].copy()
    diff = np.sqrt(np.sum((crop - bg_color)**2, axis=-1))
    
    # Corners are background, icon center has high diff
    # Soft alpha based on color diff from dark blue background
    alpha = np.clip((diff - 14.0) / 22.0 * 255.0, 0, 255)
    
    # Clean edges
    yy, xx = np.ogrid[:2*r, :2*r]
    dist_border = np.sqrt((xx - r)**2 + (yy - r)**2)
    border_fade = np.clip((r - dist_border) / 3.0, 0, 1)
    alpha = alpha * border_fade
    
    rgba = np.dstack([crop.astype(np.uint8), alpha.astype(np.uint8)])
    icon_img = Image.fromarray(rgba, mode='RGBA')
    # Resize with smooth lanczos to 80x80 for crisp display on high-DPI screens
    icon_img = icon_img.resize((80, 80), Image.Resampling.LANCZOS)
    icon_img.save(os.path.join(out_dir, f'{name}.png'))
    print(f'Processed {name}.png')

print('All 10 authentic gift logos extracted and matted cleanly!')
