import numpy as np
from PIL import Image, ImageDraw, ImageFilter

w, h = 1493, 2000
cx_m, cy_m = 745, 694
mw, mh = 170, 70

mouth_open = Image.new('RGBA', (w, h), (0, 0, 0, 0))
draw = ImageDraw.Draw(mouth_open)

lip_c = (60, 26, 18, 255)
cavity_c = (112, 30, 42, 255)
tongue_c = (248, 118, 128, 255)

# Bounding box of ellipse: top at cy_m - 10, bottom at cy_m + mh
# A cute smiling open mouth:
# We draw the polygon of the mouth:
# Top curve (smiling):
xs = np.linspace(cx_m - mw//2, cx_m + mw//2, 40)
# Top lip smile curve (slight downward dip in center or slight smile)
top_pts = []
for x in xs:
    dx = (x - cx_m) / (mw / 2.0)
    # Smile curve: corners are slightly higher than center
    dy = 6.0 * (dx**2 - 1.0) # at center dx=0, dy = -6. at edges dx=1, dy=0
    top_pts.append((x, cy_m + dy))

# Bottom lip deep curve:
bot_pts = []
for x in reversed(xs):
    dx = (x - cx_m) / (mw / 2.0)
    dy = mh * (1.0 - dx**2)
    bot_pts.append((x, cy_m + dy))

mouth_polygon = top_pts + bot_pts
draw.polygon(mouth_polygon, fill=cavity_c, outline=lip_c)

# Cute tongue at bottom
tongue_xs = np.linspace(cx_m - mw//3, cx_m + mw//3, 30)
t_top = []
for x in tongue_xs:
    dx = (x - cx_m) / (mw / 3.0)
    t_top.append((x, cy_m + mh * 0.45 - 5 * (1.0 - dx**2)))
t_bot = []
for x in reversed(tongue_xs):
    dx = (x - cx_m) / (mw / 3.0)
    t_bot.append((x, cy_m + mh * 0.95 * (1.0 - dx**2 * 0.3)))

draw.polygon(t_top + t_bot, fill=tongue_c)

# Clean outline around the mouth
for i in range(len(mouth_polygon)):
    p1 = mouth_polygon[i]
    p2 = mouth_polygon[(i+1)%len(mouth_polygon)]
    draw.line([p1, p2], fill=lip_c, width=7)

mouth_open = mouth_open.filter(ImageFilter.GaussianBlur(0.6))
mouth_open.save(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\rig\mouth_open.png')
print('Fixed mouth_open.png')

# Now verify composite!
body = Image.open(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\rig\body_clean.png')
eyes = Image.open(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\rig\pupils_default.png')
comp = body.copy()
comp.paste(eyes, (0, 0), mask=eyes)
comp.paste(mouth_open, (0, 0), mask=mouth_open)
comp.save(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\rig\comp_2_open_fixed.png')
print('Verified comp_2_open_fixed.png')
