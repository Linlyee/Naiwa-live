import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def perfect_talking(out_dir):
    idle = Image.open(os.path.join(out_dir, 'idle.png')).convert('RGBA')
    talking = idle.copy()
    draw = ImageDraw.Draw(talking)
    
    # Original mouth line: y: 682 to 702, x: 630 to 860. Center at x=745, y=692.
    cx, cy = 745, 688
    mw, mh = 190, 85
    
    # Colors matching the character's 3D shading
    lip_color = (62, 30, 20, 255)
    inner_mouth = (118, 32, 42, 255)
    tongue_color = (248, 120, 130, 255)
    
    # 1. Draw mouth cavity: downward opening semi-ellipse
    mouth_box = [cx - mw//2, cy - 2, cx + mw//2, cy + mh]
    draw.chord(mouth_box, start=0, end=180, fill=inner_mouth, outline=lip_color, width=6)
    
    # 2. Draw cute pink tongue in lower part
    tw, th = 120, 50
    tongue_box = [cx - tw//2, cy + mh - th + 5, cx + tw//2, cy + mh + 15]
    draw.chord(tongue_box, start=0, end=180, fill=tongue_color)
    
    # 3. Top lip line cleanly defining the upper smile boundary
    # Slight arc curving upwards at the corners
    points = []
    for x in np.linspace(cx - mw//2 - 5, cx + mw//2 + 5, 50):
        # subtle curve
        dx = (x - cx) / (mw/2)
        dy = -5 * (1 - dx**2) # slight upward curve in center
        points.append((x, cy + dy))
    
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=lip_color, width=6)
        
    out_path = os.path.join(out_dir, 'talking.png')
    talking.save(out_path)
    print("Perfect talking.png saved")

def perfect_sleep(out_dir):
    idle = Image.open(os.path.join(out_dir, 'idle.png')).convert('RGBA')
    arr = np.array(idle)
    
    # Left eye: pupil center (540, 538), radius ~ 65. Socket radius ~ 95.
    # Right eye: pupil center (955, 538), radius ~ 65. Socket radius ~ 95.
    # Let's inspect the yellow ring:
    # Instead of blurring whole area, we can fill the pupil with the socket ring color,
    # then apply a smooth radial gradient so it looks like a closed eyelid!
    
    sleep = idle.copy()
    draw = ImageDraw.Draw(sleep)
    
    for (cx, cy) in [(540, 538), (955, 538)]:
        # Pupil radius is 60.
        # Sample socket color at r=70 (it's around (242, 235, 140))
        # Fill pupil area
        pupil_mask = Image.new('L', idle.size, 0)
        pdraw = ImageDraw.Draw(pupil_mask)
        pdraw.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], fill=255)
        pupil_mask = pupil_mask.filter(ImageFilter.GaussianBlur(8))
        
        # Color of eyelid matching surrounding socket: (244, 236, 142, 255)
        eyelid_color_layer = Image.new('RGBA', idle.size, (246, 238, 144, 255))
        sleep.paste(eyelid_color_layer, (0, 0), mask=pupil_mask)
        
        # Now draw the closed sleeping eye line (like in anime / chibi 3D art)
        # It runs across the eyelid naturally
        eye_col = (68, 35, 24, 255)
        draw.arc([cx - 55, cy - 25, cx + 55, cy + 35], start=205, end=335, fill=eye_col, width=11)
        # Cute lash at outer corner
        if cx < 700:
            draw.line([cx - 50, cy - 5, cx - 72, cy - 10], fill=eye_col, width=8)
        else:
            draw.line([cx + 50, cy - 5, cx + 72, cy - 10], fill=eye_col, width=8)
            
    out_path = os.path.join(out_dir, 'sleep.png')
    sleep.save(out_path)
    print("Perfect sleep.png saved")

if __name__ == '__main__':
    perfect_talking(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets')
    perfect_sleep(r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets')
