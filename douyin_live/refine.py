import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def refine_talking_and_sleep(out_dir):
    idle_path = os.path.join(out_dir, 'idle.png')
    idle = Image.open(idle_path)
    
    # 1. REFINE TALKING
    talking = idle.copy()
    draw = ImageDraw.Draw(talking)
    
    # Mouth location: center (745, 693)
    # Original mouth ends around x=630 to 860
    cx, cy = 745, 693
    
    # First, smooth out the original mouth slit with skin clone
    skin_sample = idle.crop((cx - 130, cy - 60, cx + 130, cy - 20)).resize((260, 40)).filter(ImageFilter.GaussianBlur(5))
    talking.paste(skin_sample, (cx - 130, cy - 15), mask=Image.new('L', (260, 40), 220))
    
    # Draw open smiling mouth:
    # Top lip is a slightly curved smile line, bottom curves downward
    # Outer dark lip
    lip_color = (65, 32, 22, 255)
    inner_mouth = (115, 35, 45, 255)
    tongue_color = (245, 115, 125, 255)
    
    # Mouth polygon/chord:
    mw, mh = 170, 95
    mouth_box = [cx - mw//2, cy - 10, cx + mw//2, cy + mh]
    draw.chord(mouth_box, start=0, end=180, fill=inner_mouth, outline=lip_color, width=7)
    
    # Tongue:
    tw, th = 110, 60
    tongue_box = [cx - tw//2, cy + mh - th + 5, cx + tw//2, cy + mh + 20]
    draw.chord(tongue_box, start=0, end=180, fill=tongue_color)
    
    # Cute little teeth at upper mouth edge:
    draw.rectangle([cx - 40, cy - 5, cx + 40, cy + 12], fill=(255, 255, 250, 240))
    # Redraw upper lip line cleanly
    draw.line([cx - mw//2 - 5, cy, cx + mw//2 + 5, cy], fill=lip_color, width=7)
    
    talking_path = os.path.join(out_dir, 'talking.png')
    talking.save(talking_path)
    print("Refined talking.png")
    
    # 2. REFINE SLEEP
    sleep = idle.copy()
    draw_s = ImageDraw.Draw(sleep)
    
    # For eyes: left center (540, 538), right center (955, 538)
    # Eye radius with outer socket is ~105
    er = 105
    
    # Sample forehead skin
    forehead = idle.crop((700, 340, 850, 490)).resize((er * 2 + 20, er * 2 + 20)).filter(ImageFilter.GaussianBlur(12))
    
    # Soft feathered circular mask
    mask = Image.new('L', (er * 2 + 20, er * 2 + 20), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse([10, 10, er * 2 + 10, er * 2 + 10], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(14))
    
    sleep.paste(forehead, (540 - er - 10, 538 - er - 10), mask=mask)
    sleep.paste(forehead, (955 - er - 10, 538 - er - 10), mask=mask)
    
    # Draw dark brown sleeping curve (^_^ style closed eye arcs)
    eye_col = (68, 35, 24, 255)
    # Left eye curve
    draw_s.arc([540 - 70, 538 - 35, 540 + 70, 538 + 45], start=205, end=335, fill=eye_col, width=12)
    # Right eye curve
    draw_s.arc([955 - 70, 538 - 35, 955 + 70, 538 + 45], start=205, end=335, fill=eye_col, width=12)
    
    # Lashes at edge
    draw_s.line([540 - 62, 538 - 5, 540 - 85, 538 - 10], fill=eye_col, width=9)
    draw_s.line([955 + 62, 538 - 5, 955 + 85, 538 - 10], fill=eye_col, width=9)
    
    sleep_path = os.path.join(out_dir, 'sleep.png')
    sleep.save(sleep_path)
    print("Refined sleep.png")

if __name__ == '__main__':
    refine_talking_and_sleep(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets')
