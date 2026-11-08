import numpy as np
from PIL import Image, ImageFilter

src_path = r'C:/Users/林夏/.gemini/antigravity-cli/brain/651b12b7-4f61-4712-aae0-11039f1a14a6/.user_uploaded/uploaded_media_1793432806879.jpg'
img = Image.open(src_path).convert('RGB')
arr = np.array(img, dtype=float)
h, w, _ = arr.shape

# 1. Clean background alpha
bg_ref = np.array([254.0, 254.0, 253.5])
diff = np.sqrt(np.sum((arr - bg_ref)**2, axis=-1))

y_coords = np.arange(h)[:, None]
alpha = np.clip((diff - 8.0) / 16.0 * 255.0, 0, 255)
shadow_fade = np.clip((1735 - y_coords) / 25.0, 0, 1)
alpha = alpha * shadow_fade

semi_mask = (alpha > 0) & (alpha < 255)
alpha_norm = (alpha / 255.0)[:, :, None]
rgb = arr.copy()
rgb[semi_mask] = np.clip((rgb[semi_mask] - (1.0 - alpha_norm[semi_mask]) * bg_ref) / np.maximum(alpha_norm[semi_mask], 0.05), 0, 255)

# 2. Completely eliminate the mouth slit:
# Original slit is inside x: 620 to 870, y: 680 to 710
# We take a skin region around it:
# For every pixel inside x: 600 to 890, y: 672 to 718:
# We directly interpolate between y=665 (clean skin above) and y=725 (clean skin below)
y_top, y_bot = 665, 725
x_left, x_right = 590, 900

top_row = rgb[y_top, x_left:x_right, :] # (310, 3)
bot_row = rgb[y_bot, x_left:x_right, :] # (310, 3)

for y in range(670, 720):
    t = (y - y_top) / (y_bot - y_top)
    # Direct replacement across the mouth line!
    rgb[y, x_left:x_right, :] = (1.0 - t) * top_row + t * bot_row

# Apply a gentle horizontal blur on the patched region to make lighting 100% natural
patch = Image.fromarray(rgb[660:730, 580:910].astype(np.uint8))
patch = patch.filter(ImageFilter.GaussianBlur(3.5))
rgb[660:730, 580:910] = np.array(patch)

# 3. Clean eye sockets:
for cx, cy in [(540, 538), (955, 538)]:
    # Socket rim radius ~ 75
    # Sample clean socket ring
    yy, xx = np.ogrid[:h, :w]
    dist = np.sqrt((xx - cx)**2 + (yy - cy)**2)
    # Uniform fill inside pupil (dist < 65) with socket ring color [245, 237, 142]
    socket_col = np.array([245.0, 237.0, 142.0])
    pupil_mask = np.clip((68 - dist) / 6.0, 0, 1)[:, :, None]
    rgb = (1.0 - pupil_mask) * rgb + pupil_mask * socket_col

rgba = np.dstack([rgb.astype(np.uint8), alpha.astype(np.uint8)])
body_clean = Image.fromarray(rgba, mode='RGBA')
body_clean.save(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\rig\body_clean.png')
print('Flawless body_clean saved')
