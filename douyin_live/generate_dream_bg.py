import numpy as np
from PIL import Image, ImageDraw, ImageFilter

w, h = 1080, 1920

y_coords = np.linspace(0, 1, h)[:, None]
x_coords = np.linspace(0, 1, w)[None, :]

# Vertical color gradient:
# Deep marine twilight with center stage illumination
r_grad = 10 * (1 - y_coords) + 22 * np.exp(-((y_coords - 0.42)**2) / 0.12) + 6 * y_coords
g_grad = 24 * (1 - y_coords) + 48 * np.exp(-((y_coords - 0.42)**2) / 0.12) + 16 * y_coords
b_grad = 42 * (1 - y_coords) + 75 * np.exp(-((y_coords - 0.42)**2) / 0.12) + 28 * y_coords

bg_r = np.tile(r_grad, (1, w))
bg_g = np.tile(g_grad, (1, w))
bg_b = np.tile(b_grad, (1, w))

# Add soft radial glow at center stage
dist_center = np.sqrt((x_coords - 0.5)**2 * 1.5 + (y_coords - 0.42)**2)
center_glow = np.exp(-(dist_center**2) / 0.16)

bg_r += center_glow * 25.0
bg_g += center_glow * 50.0
bg_b += center_glow * 80.0

bg_arr = np.dstack([bg_r, bg_g, bg_b])
bg_arr = np.clip(bg_arr, 0, 255).astype(np.uint8)
bg_img = Image.fromarray(bg_arr, mode='RGB')

# Draw soft floating underwater / musical orbs
draw = ImageDraw.Draw(bg_img, 'RGBA')
np.random.seed(42)

for _ in range(40):
    bx = np.random.randint(40, w - 40)
    by = np.random.randint(80, h - 150)
    br = np.random.randint(10, 55)
    alpha = np.random.randint(20, 50)
    
    orb = Image.new('RGBA', (br * 2, br * 2), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(orb)
    odraw.ellipse([2, 2, br * 2 - 4, br * 2 - 4], fill=(150, 215, 255, alpha), outline=(230, 245, 255, int(alpha * 1.6)), width=2)
    orb = orb.filter(ImageFilter.GaussianBlur(3))
    bg_img.paste(orb, (bx - br, by - br), mask=orb)

out_path = r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\live_bg.jpg'
bg_img.save(out_path, quality=95)
print('Generated dreamscape background successfully:', out_path)
