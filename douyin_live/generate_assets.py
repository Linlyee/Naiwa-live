import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def make_idle(src_path, out_dir):
    img = Image.open(src_path).convert('RGB')
    arr = np.array(img, dtype=float)
    h, w, _ = arr.shape
    
    # Background distance
    bg_ref = np.array([254.0, 254.0, 253.5])
    diff = np.sqrt(np.sum((arr - bg_ref)**2, axis=-1))
    
    # Below y=1720, fade out any ground shadow
    y_coords = np.arange(h)[:, None]
    
    # Calculate alpha with anti-aliasing
    # diff <= 8 -> 0
    # diff >= 24 -> 255
    alpha = np.clip((diff - 8.0) / 16.0 * 255.0, 0, 255)
    
    # Fade shadow below feet
    shadow_fade = np.clip((1735 - y_coords) / 25.0, 0, 1)
    alpha = alpha * shadow_fade
    
    # Remove white fringing by adjusting RGB where alpha is semi-transparent
    semi_mask = (alpha > 0) & (alpha < 255)
    alpha_norm = (alpha / 255.0)[:, :, None]
    
    # De-multiply white background
    rgb = arr.copy()
    rgb[semi_mask] = np.clip((rgb[semi_mask] - (1.0 - alpha_norm[semi_mask]) * bg_ref) / np.maximum(alpha_norm[semi_mask], 0.05), 0, 255)
    
    rgba = np.dstack([rgb.astype(np.uint8), alpha.astype(np.uint8)])
    idle_img = Image.fromarray(rgba, mode='RGBA')
    
    out_path = os.path.join(out_dir, 'idle.png')
    idle_img.save(out_path, format='PNG')
    print(f"Created {out_path}")
    return idle_img

def make_talking(base_img, out_dir):
    # Create talking version with open mouth
    talking = base_img.copy()
    draw = ImageDraw.Draw(talking)
    
    # Mouth center is around x=745, y=695
    # Original mouth is from x=630 to 860, y=682 to 702
    cx, cy = 745, 695
    mw, mh = 160, 110 # width and height of open mouth
    
    # First, overpaint the thin line mouth with skin color patch
    # Sample surrounding skin color around (745, 650)
    skin_patch = base_img.crop((cx - 150, cy - 40, cx + 150, cy + 40)).filter(ImageFilter.GaussianBlur(8))
    talking.paste(skin_patch, (cx - 150, cy - 40), mask=Image.new('L', (300, 80), 200))
    
    # Draw open mouth
    # Mouth outline (dark brown lip)
    lip_color = (68, 38, 28, 255)
    inner_mouth = (112, 36, 42, 255)
    tongue_color = (238, 118, 126, 255)
    
    # Draw dark mouth cavity: a cute rounded D-shape or bean shape
    mouth_box = [cx - mw//2, cy - mh//2 + 5, cx + mw//2, cy + mh//2 + 15]
    draw.chord(mouth_box, start=0, end=180, fill=inner_mouth, outline=lip_color, width=6)
    
    # Draw tongue inside bottom of mouth
    tongue_box = [cx - mw//3, cy + 5, cx + mw//3, cy + mh//2 + 12]
    draw.chord(tongue_box, start=0, end=180, fill=tongue_color)
    
    # Subtle upper tooth or lip highlight
    tooth_box = [cx - mw//4, cy - mh//2 + 7, cx + mw//4, cy - mh//2 + 22]
    draw.chord(tooth_box, start=0, end=180, fill=(255, 255, 250, 230))
    
    # Soft blur on edges of mouth overlay to blend with 3D skin
    out_path = os.path.join(out_dir, 'talking.png')
    talking.save(out_path, format='PNG')
    print(f"Created {out_path}")
    return talking

def make_sleep(base_img, out_dir):
    # Create sleep version with closed smiling eyes and Zzz
    sleep_img = base_img.copy()
    draw = ImageDraw.Draw(sleep_img)
    
    # Eye centers:
    # Left eye: x=540, y=538
    # Right eye: x=955, y=538
    # Eye radius ~ 65
    left_cx, left_cy = 540, 538
    right_cx, right_cy = 955, 538
    er = 75
    
    # Cover the black eyes with smooth yellow skin texture from above forehead
    skin_src = base_img.crop((700, 360, 850, 510)).resize((er * 2 + 30, er * 2 + 30)).filter(ImageFilter.GaussianBlur(10))
    
    # Circular mask for eye area
    mask = Image.new('L', (er * 2 + 30, er * 2 + 30), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([5, 5, er * 2 + 25, er * 2 + 25], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(4))
    
    sleep_img.paste(skin_src, (left_cx - er - 15, left_cy - er - 15), mask=mask)
    sleep_img.paste(skin_src, (right_cx - er - 15, right_cy - er - 15), mask=mask)
    
    # Now draw cute smiling closed eyes (curved lines: ⌒ ⌒)
    eye_line_color = (75, 42, 30, 255)
    
    # Left eye curve
    draw.arc([left_cx - 55, left_cy - 30, left_cx + 55, left_cy + 40], start=200, end=340, fill=eye_line_color, width=10)
    # Right eye curve
    draw.arc([right_cx - 55, right_cy - 30, right_cx + 55, right_cy + 40], start=200, end=340, fill=eye_line_color, width=10)
    
    # Draw cute eyelashes at corners
    draw.line([left_cx - 45, left_cy - 10, left_cx - 65, left_cy - 5], fill=eye_line_color, width=8)
    draw.line([right_cx + 45, right_cy - 10, right_cx + 65, right_cy - 5], fill=eye_line_color, width=8)
    
    out_path = os.path.join(out_dir, 'sleep.png')
    sleep_img.save(out_path, format='PNG')
    print(f"Created {out_path}")
    return sleep_img

def make_squish(base_img, out_dir):
    # Squashed / flattened pancake character (心动压扁)
    # Compress vertically to 0.45, expand horizontally to 1.35
    w, h = base_img.size
    new_w = int(w * 1.35)
    new_h = int(h * 0.48)
    squished = base_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Create canvas of same height to maintain alignment at feet
    canvas = Image.new('RGBA', (new_w, h), (0, 0, 0, 0))
    # Place squished character resting on the ground
    canvas.paste(squished, (0, h - new_h - 100))
    
    # Draw dizzy cartoon spiral eyes on the squished face!
    draw = ImageDraw.Draw(canvas)
    # Find new eye locations on squished face
    squish_cy = h - new_h - 100 + int(538 * 0.48)
    left_cx = int(540 * 1.35)
    right_cx = int(955 * 1.35)
    
    # Draw dizzy swirls (@_@)
    spiral_color = (60, 30, 20, 240)
    for cx in [left_cx, right_cx]:
        # Cover pupil center with yellow skin
        draw.ellipse([cx - 40, squish_cy - 25, cx + 40, squish_cy + 25], fill=(255, 235, 120, 255))
        # Draw concentric/spiral arcs
        draw.arc([cx - 35, squish_cy - 20, cx + 35, squish_cy + 20], start=0, end=270, fill=spiral_color, width=7)
        draw.arc([cx - 22, squish_cy - 14, cx + 22, squish_cy + 14], start=90, end=360, fill=spiral_color, width=6)
        draw.arc([cx - 10, squish_cy - 8, cx + 10, squish_cy + 8], start=180, end=450, fill=spiral_color, width=5)
    
    out_path = os.path.join(out_dir, 'squish.png')
    canvas.save(out_path, format='PNG')
    print(f"Created {out_path}")
    return canvas

def make_bloat(base_img, out_dir):
    # Bloated / full belly character (贪吃过载)
    # Belly swells outward into a big round dumpling
    w, h = base_img.size
    bloated = base_img.copy()
    
    # Scale middle and lower body
    # Using pillow mesh or selective scaling
    # We can widen the body by 1.25x while keeping head relatively normal
    arr = np.array(base_img)
    # Stretch x coordinates non-linearly based on y (belly between y=800 and 1500)
    # Let's perform a smooth barrel warp on the belly region
    h_b, w_b = h, int(w * 1.2)
    canvas = Image.new('RGBA', (w_b, h), (0, 0, 0, 0))
    offset_x = (w_b - w) // 2
    
    # Resize slightly wider and taller
    resized = base_img.resize((int(w * 1.18), int(h * 1.05)), Image.Resampling.LANCZOS)
    rw, rh = resized.size
    canvas.paste(resized, ((w_b - rw)//2, h - rh))
    
    # Add a cute full smile (satisfied food expression) and crumbs
    draw = ImageDraw.Draw(canvas)
    cx = w_b // 2
    cy = int(695 * 1.05) + (h - rh)
    
    # Satisfied closed smile
    smile_color = (70, 35, 25, 255)
    draw.arc([cx - 70, cy - 30, cx + 70, cy + 25], start=20, end=160, fill=smile_color, width=9)
    
    out_path = os.path.join(out_dir, 'bloat.png')
    canvas.save(out_path, format='PNG')
    print(f"Created {out_path}")
    return canvas

def make_blush(base_img, out_dir):
    # Deep blush & heart eyes / extra cute (夸夸/害羞)
    blush_img = base_img.copy()
    draw = ImageDraw.Draw(blush_img)
    
    # Cheeks: left (540, 620), right (955, 620)
    for cx in [530, 965]:
        # Draw glowing pink oval
        blush_oval = Image.new('RGBA', (220, 140), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(blush_oval)
        bdraw.ellipse([10, 10, 210, 130], fill=(255, 80, 110, 130))
        blush_oval = blush_oval.filter(ImageFilter.GaussianBlur(15))
        blush_img.paste(blush_oval, (cx - 110, 620 - 70), mask=blush_oval)
        
        # Draw cute anime blush slash marks (///)
        draw.line([cx - 45, 635, cx - 30, 605], fill=(220, 50, 80, 220), width=6)
        draw.line([cx - 20, 638, cx - 5, 608], fill=(220, 50, 80, 220), width=6)
        draw.line([cx + 5, 640, cx + 20, 610], fill=(220, 50, 80, 220), width=6)
        draw.line([cx + 30, 637, cx + 45, 607], fill=(220, 50, 80, 220), width=6)
        
    out_path = os.path.join(out_dir, 'blush.png')
    blush_img.save(out_path, format='PNG')
    print(f"Created {out_path}")
    return blush_img

if __name__ == '__main__':
    src = r'C:/Users/林夏/.gemini/antigravity-cli/brain/651b12b7-4f61-4712-aae0-11039f1a14a6/.user_uploaded/uploaded_media_1793432806879.jpg'
    out = r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets'
    
    print('Processing idle...')
    idle = make_idle(src, out)
    
    print('Processing talking...')
    make_talking(idle, out)
    
    print('Processing sleep...')
    make_sleep(idle, out)
    
    print('Processing squish...')
    make_squish(idle, out)
    
    print('Processing bloat...')
    make_bloat(idle, out)
    
    print('Processing blush...')
    make_blush(idle, out)
    
    print('All character states generated successfully!')
