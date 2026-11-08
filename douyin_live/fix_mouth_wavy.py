import numpy as np
from PIL import Image, ImageDraw, ImageFilter

w, h = 1493, 2000
cx_m, cy_m = 745, 695

mouth_wavy = Image.new('RGBA', (w, h), (0, 0, 0, 0))
draw = ImageDraw.Draw(mouth_wavy)
lip_c = (60, 26, 18, 255)

w_pts = []
for x in np.linspace(cx_m - 80, cx_m + 80, 50):
    phase = (x - (cx_m - 80)) / 160.0 * 4 * np.pi
    dy = 12 * np.sin(phase)
    w_pts.append((x, cy_m + dy))
for i in range(len(w_pts)-1):
    draw.line([w_pts[i], w_pts[i+1]], fill=lip_c, width=8)

mouth_wavy = mouth_wavy.filter(ImageFilter.GaussianBlur(0.6))
mouth_wavy.save(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\rig\mouth_wavy.png')

# Composite test with dizzy eyes
body = Image.open(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\rig\body_clean.png')
eyes_dizzy = Image.open(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\rig\eyes_dizzy.png')
comp = body.copy()
comp.paste(eyes_dizzy, (0, 0), mask=eyes_dizzy)
comp.paste(mouth_wavy, (0, 0), mask=mouth_wavy)
comp.save(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\rig\comp_4_dizzy.png')
print('comp_4_dizzy saved')
