import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def create_layers():
    src_path = r'C:/Users/林夏/.gemini/antigravity-cli/brain/651b12b7-4f61-4712-aae0-11039f1a14a6/.user_uploaded/uploaded_media_1793432806879.jpg'
    out_dir = r'D:\zhibo\Open-LLM-VTuber\douyin_live\assets\rig'
    os.makedirs(out_dir, exist_ok=True)
    
    img = Image.open(src_path).convert('RGB')
    arr = np.array(img, dtype=float)
    h, w, _ = arr.shape
    
    # 1. Clean transparent body
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
    
    rgba = np.dstack([rgb.astype(np.uint8), alpha.astype(np.uint8)])
    base_body = Image.fromarray(rgba, mode='RGBA')
    
    # 2. Extract Pupil Left & Pupil Right
    # Left eye: center (540, 538)
    # Right eye: center (955, 538)
    # We will save full canvas overlay layers so positioning in CSS is 100% exact (width: 100%, height: 100%)
    
    # Pupil Left Layer
    pupil_left_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    # Crop pupil area around 540, 538
    cx_l, cy_l = 540, 538
    r = 65
    p_crop_l = base_body.crop((cx_l - r, cy_l - r, cx_l + r, cy_l + r))
    # Mask to keep only the dark pupil and highlight
    p_arr_l = np.array(p_crop_l)
    # Pupil has low red/green/blue OR white highlight
    is_pupil = (p_arr_l[:,:,0] < 80) & (p_arr_l[:,:,1] < 80) & (p_arr_l[:,:,2] < 80)
    # highlight is pure white
    is_highlight = (p_arr_l[:,:,0] > 230) & (p_arr_l[:,:,1] > 230) & (p_arr_l[:,:,2] > 230)
    pupil_mask = is_pupil | is_highlight
    # circular bound
    yy, xx = np.ogrid[:2*r, :2*r]
    dist_sq = (xx - r)**2 + (yy - r)**2
    pupil_mask = pupil_mask & (dist_sq <= (r-2)**2)
    
    p_rgba_l = p_arr_l.copy()
    p_rgba_l[~pupil_mask, 3] = 0
    p_img_l = Image.fromarray(p_rgba_l, mode='RGBA').filter(ImageFilter.GaussianBlur(0.5))
    pupil_left_layer.paste(p_img_l, (cx_l - r, cy_l - r), mask=p_img_l)
    pupil_left_layer.save(os.path.join(out_dir, 'pupil_left.png'))
    
    # Pupil Right Layer
    pupil_right_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    cx_r, cy_r = 955, 538
    p_crop_r = base_body.crop((cx_r - r, cy_r - r, cx_r + r, cy_r + r))
    p_arr_r = np.array(p_crop_r)
    is_pupil_r = (p_arr_r[:,:,0] < 80) & (p_arr_r[:,:,1] < 80) & (p_arr_r[:,:,2] < 80)
    is_highlight_r = (p_arr_r[:,:,0] > 230) & (p_arr_r[:,:,1] > 230) & (p_arr_r[:,:,2] > 230)
    pupil_mask_r = (is_pupil_r | is_highlight_r) & (dist_sq <= (r-2)**2)
    p_rgba_r = p_arr_r.copy()
    p_rgba_r[~pupil_mask_r, 3] = 0
    p_img_r = Image.fromarray(p_rgba_r, mode='RGBA').filter(ImageFilter.GaussianBlur(0.5))
    pupil_right_layer.paste(p_img_r, (cx_r - r, cy_r - r), mask=p_img_r)
    pupil_right_layer.save(os.path.join(out_dir, 'pupil_right.png'))
    
    # Both pupils combined:
    pupils_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    pupils_layer.paste(pupil_left_layer, (0, 0), mask=pupil_left_layer)
    pupils_layer.paste(pupil_right_layer, (0, 0), mask=pupil_right_layer)
    pupils_layer.save(os.path.join(out_dir, 'pupils_default.png'))
    
    # 3. Create Eyes Closed / Happy (^ _ ^)
    eyes_happy = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw_h = ImageDraw.Draw(eyes_happy)
    eye_col = (72, 38, 26, 255)
    for cx, cy in [(cx_l, cy_l), (cx_r, cy_r)]:
        # Draw smooth crescent smiling arc
        points = []
        for x in np.linspace(cx - 52, cx + 52, 40):
            dx = (x - cx) / 52.0
            dy = 18 * (1.0 - dx**2)
            points.append((x, cy + 4 - dy))
        for i in range(len(points)-1):
            draw_h.line([points[i], points[i+1]], fill=eye_col, width=10)
        # eyelash
        if cx < 700:
            draw_h.line([cx - 48, cy + 4, cx - 70, cy], fill=eye_col, width=8)
        else:
            draw_h.line([cx + 48, cy + 4, cx + 70, cy], fill=eye_col, width=8)
    eyes_happy = eyes_happy.filter(ImageFilter.GaussianBlur(0.6))
    eyes_happy.save(os.path.join(out_dir, 'eyes_happy.png'))
    
    # 4. Create Spiral Dizzy Eyes (@ _ @) for squish / damage
    eyes_dizzy = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw_d = ImageDraw.Draw(eyes_dizzy)
    dizzy_col = (72, 36, 24, 255)
    for cx, cy in [(cx_l, cy_l), (cx_r, cy_r)]:
        # Draw 3-turn smooth spiral
        t = np.linspace(0, 4.5 * np.pi, 120)
        r_spiral = 4 + 3.8 * t
        xs = cx + r_spiral * np.cos(t)
        ys = cy + r_spiral * np.sin(t)
        for i in range(len(xs)-1):
            draw_d.line([(xs[i], ys[i]), (xs[i+1], ys[i+1])], fill=dizzy_col, width=8)
    eyes_dizzy = eyes_dizzy.filter(ImageFilter.GaussianBlur(0.6))
    eyes_dizzy.save(os.path.join(out_dir, 'eyes_dizzy.png'))

    # 5. Create Star Sparkle Eyes (★ _ ★) for Gifts
    eyes_star = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(eyes_star)
    star_col = (255, 215, 0, 255)
    star_inner = (255, 255, 220, 255)
    for cx, cy in [(cx_l, cy_l), (cx_r, cy_r)]:
        # 4-pointed sparkle
        r_star = 45
        pts = [
            (cx, cy - r_star), (cx + 12, cy - 12), (cx + r_star, cy), (cx + 12, cy + 12),
            (cx, cy + r_star), (cx - 12, cy + 12), (cx - r_star, cy), (cx - 12, cy - 12)
        ]
        draw_s.polygon(pts, fill=star_col)
        # inner highlight
        pts_in = [
            (cx, cy - r_star//2), (cx + 6, cy - 6), (cx + r_star//2, cy), (cx + 6, cy + 6),
            (cx, cy + r_star//2), (cx - 6, cy + 6), (cx - r_star//2, cy), (cx - 6, cy - 6)
        ]
        draw_s.polygon(pts_in, fill=star_inner)
    eyes_star = eyes_star.filter(ImageFilter.GaussianBlur(0.8))
    eyes_star.save(os.path.join(out_dir, 'eyes_star.png'))

    # 6. Extract Default Mouth Layer
    mouth_default = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    # Mouth region: x 620 to 870, y 675 to 715
    m_crop = base_body.crop((610, 670, 880, 720))
    m_arr = np.array(m_crop)
    # Mask mouth slit: where R < 165 and G < 130
    is_slit = (m_arr[:,:,0] < 165) & (m_arr[:,:,1] < 130) & (m_arr[:,:,2] < 90)
    m_rgba = m_arr.copy()
    m_rgba[~is_slit, 3] = 0
    m_img = Image.fromarray(m_rgba, mode='RGBA').filter(ImageFilter.GaussianBlur(0.6))
    mouth_default.paste(m_img, (610, 670), mask=m_img)
    mouth_default.save(os.path.join(out_dir, 'mouth_neutral.png'))

    # 7. Create 3D Rendered Talking Mouth: Wide Open Happy Mouth
    # Centered at x=745, y=695
    mouth_open = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw_mo = ImageDraw.Draw(mouth_open)
    cx_m, cy_m = 745, 693
    mw, mh = 175, 75
    
    lip_c = (65, 30, 20, 255)
    cavity_c = (112, 32, 42, 255)
    tongue_c = (248, 120, 130, 255)
    
    # Outer cavity
    draw_mo.chord([cx_m - mw//2, cy_m - 4, cx_m + mw//2, cy_m + mh*2], start=0, end=180, fill=cavity_c, outline=lip_c, width=7)
    # Tongue
    draw_mo.chord([cx_m - 50, cy_m + mh - 25, cx_m + 50, cy_m + mh*2 + 10], start=0, end=180, fill=tongue_c)
    # Upper lip line
    draw_mo.line([cx_m - mw//2 - 5, cy_m, cx_m + mw//2 + 5, cy_m], fill=lip_c, width=7)
    mouth_open = mouth_open.filter(ImageFilter.GaussianBlur(0.6))
    mouth_open.save(os.path.join(out_dir, 'mouth_open.png'))

    # 8. Create "O" Mouth (Surprised / Ooh)
    mouth_o = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw_o = ImageDraw.Draw(mouth_o)
    draw_o.ellipse([cx_m - 38, cy_m - 10, cx_m + 38, cy_m + 65], fill=cavity_c, outline=lip_c, width=7)
    draw_o.ellipse([cx_m - 20, cy_m + 25, cx_m + 20, cy_m + 58], fill=tongue_c)
    mouth_o = mouth_o.filter(ImageFilter.GaussianBlur(0.6))
    mouth_o.save(os.path.join(out_dir, 'mouth_o.png'))

    # 9. Create Wavy Dizzy Mouth (~~~ for squish)
    mouth_wavy = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw_w = ImageDraw.Draw(mouth_wavy)
    w_pts = []
    for x in np.linspace(cx_m - 80, cx_m + 80, 50):
        phase = (x - (cx_m - 80)) / 160.0 * 4 * np.pi
        dy = 12 * np.sin(phase)
        w_pts.append((x, cy_m + 5 + dy))
    for i in range(len(w_pts)-1):
        draw_w.line([w_pts[i], w_pts[i+1]], fill=lip_c, width=8)
    mouth_wavy = mouth_wavy.filter(ImageFilter.GaussianBlur(0.6))
    mouth_wavy.save(os.path.join(out_dir, 'mouth_wavy.png'))

    # 10. Clean Body (with eye sockets filled with neutral eye socket color and mouth slit covered so overlays fit cleanly)
    body_clean = base_body.copy()
    
    # Fill mouth slit on body_clean with surrounding skin
    skin_fill = base_body.crop((cx_m - 120, cy_m - 50, cx_m + 120, cy_m - 15)).filter(ImageFilter.GaussianBlur(8))
    m_patch_mask = Image.new('L', (240, 35), 0)
    p_draw = ImageDraw.Draw(m_patch_mask)
    p_draw.ellipse([5, 5, 235, 30], fill=255)
    m_patch_mask = m_patch_mask.filter(ImageFilter.GaussianBlur(6))
    body_clean.paste(skin_fill, (cx_m - 120, cy_m - 10), mask=m_patch_mask)
    
    # Fill the black pupil holes with the eye socket color so closed eyes or stars can appear naturally
    for cx, cy in [(cx_l, cy_l), (cx_r, cy_r)]:
        eye_patch = base_body.crop((cx - 75, cy - 140, cx + 75, cy - 80)).resize((150, 150)).filter(ImageFilter.GaussianBlur(8))
        s_mask = Image.new('L', (150, 150), 0)
        s_draw = ImageDraw.Draw(s_mask)
        s_draw.ellipse([10, 10, 140, 140], fill=255)
        s_mask = s_mask.filter(ImageFilter.GaussianBlur(10))
        body_clean.paste(eye_patch, (cx - 75, cy - 75), mask=s_mask)
        
    body_clean.save(os.path.join(out_dir, 'body_clean.png'))
    print("Layered Rig assets generated successfully in:", out_dir)

if __name__ == '__main__':
    create_layers()
