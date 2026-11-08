import numpy as np
from PIL import Image, ImageDraw, ImageFilter

idle = Image.open(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\idle.png').convert('RGBA')
sleep = idle.copy()
draw = ImageDraw.Draw(sleep)

for cx, cy in [(540, 538), (955, 538)]:
    # The pupil is black, r=58. The socket is pale yellow r=95.
    # To look like natural closed 3D eyelids:
    # 1. Fill the pupil area with the eyelid skin (sampled from just above the eye, around cy-110)
    eyelid_patch = idle.crop((cx - 80, cy - 170, cx + 80, cy - 70)).resize((160, 160)).filter(ImageFilter.GaussianBlur(6))
    
    # Smooth elliptical mask for the pupil and inner socket
    mask = Image.new('L', (160, 160), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse([10, 10, 150, 150], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(12))
    
    sleep.paste(eyelid_patch, (cx - 80, cy - 80), mask=mask)
    
    # 2. Draw the eyelid crease: a soft curved smiling crease
    crease_col = (75, 40, 28, 255)
    # The curve spans from cx - 55 to cx + 55, smiling curve
    points = []
    for x in np.linspace(cx - 55, cx + 55, 40):
        # parabolic curve
        dx = (x - cx) / 55.0
        dy = 18 * (1.0 - dx**2) # downward curve (smile)
        points.append((x, cy + 5 - dy))
    
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=crease_col, width=10)
        
    # Cute little lash flick at outer corner
    if cx < 700:
        draw.line([cx - 52, cy + 5, cx - 75, cy], fill=crease_col, width=8)
    else:
        draw.line([cx + 52, cy + 5, cx + 75, cy], fill=crease_col, width=8)

sleep.save(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\sleep.png')
print('Smooth sleep.png saved')
