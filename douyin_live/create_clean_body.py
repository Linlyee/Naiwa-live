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

# 2. Seamlessly erase the mouth slit from rgb array:
# Mouth box: y: 665 to 725, x: 600 to 890
y1, y2 = 665, 725
x1, x2 = 600, 890

top_skin = rgb[y1, x1:x2, :] # shape (290, 3)
bottom_skin = rgb[y2, x1:x2, :] # shape (290, 3)

# Vertical linear interpolation across the mouth gap:
weights = np.linspace(0, 1, y2 - y1)[:, None, None] # shape (60, 1, 1)
clean_mouth_patch = (1.0 - weights) * top_skin[None, :, :] + weights * bottom_skin[None, :, :]

# Feather the edges horizontally and vertically so it blends seamlessly
patch_h, patch_w = y2 - y1, x2 - x1
feather_y = np.sin(np.linspace(0, np.pi, patch_h))[:, None]
feather_x = np.sin(np.linspace(0, np.pi, patch_w))[None, :]
feather_mask = (feather_y * feather_x)[:, :, None] # 0 at borders, 1 in center

# Blend patch into rgb
rgb[y1:y2, x1:x2, :] = (1.0 - feather_mask) * rgb[y1:y2, x1:x2, :] + feather_mask * clean_mouth_patch

# 3. Seamlessly erase the black pupils from the eye sockets:
# Left eye: pupil center (540, 538), radius ~ 65
# Right eye: pupil center (955, 538), radius ~ 65
for cx, cy in [(540, 538), (955, 538)]:
    # Eye socket ring has color around [246, 238, 144]
    # Sample the socket color around radius 68-80
    r_in, r_out = 60, 78
    yy, xx = np.ogrid[:h, :w]
    dist = np.sqrt((xx - cx)**2 + (yy - cy)**2)
    socket_mask = (dist >= r_in) & (dist <= r_out)
    avg_socket_col = rgb[socket_mask].mean(axis=0) # [246, 238, 144]
    
    # Smooth radial blend from center (r < 65) to socket ring
    fill_mask = np.clip((r_out - dist) / (r_out - r_in + 1e-5), 0, 1)[:, :, None]
    rgb = (1.0 - fill_mask) * rgb + fill_mask * avg_socket_col

rgba = np.dstack([rgb.astype(np.uint8), alpha.astype(np.uint8)])
body_clean = Image.fromarray(rgba, mode='RGBA')
body_clean.save(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\rig\body_clean.png')
print('Perfect body_clean.png saved')
