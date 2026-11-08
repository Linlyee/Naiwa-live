# -*- coding: utf-8 -*-
import ctypes
from PIL import Image

u32 = ctypes.windll.user32
g32 = ctypes.windll.gdi32

input_desk = u32.OpenInputDesktop(0, False, 0x01FF)
u32.SetThreadDesktop(input_desk)

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
found_hwnds = []

def cb(hwnd, lParam):
    length = u32.GetWindowTextLengthW(hwnd)
    if length > 0:
        buf = ctypes.create_unicode_buffer(length + 1)
        u32.GetWindowTextW(hwnd, buf, length + 1)
        title = buf.value
        cls_buf = ctypes.create_unicode_buffer(256)
        u32.GetClassNameW(hwnd, cls_buf, 256)
        cls = cls_buf.value
        if u32.IsWindowVisible(hwnd) and any(k in title for k in ['直播伴侣', '伴侣', '抖音']):
            found_hwnds.append((hwnd, title, cls))
            print(f"Candidate: HWND {hwnd}, Title: '{title}', Class: '{cls}'")
    return True

u32.EnumDesktopWindows(input_desk, WNDENUMPROC(cb), 0)
print(f"Total candidates: {len(found_hwnds)}")

class RECT(ctypes.Structure):
    _fields_ = [('left', ctypes.c_long), ('top', ctypes.c_long), ('right', ctypes.c_long), ('bottom', ctypes.c_long)]

for hwnd, title, cls in found_hwnds:
    if 'Chrome_WidgetWin' in cls and '直播伴侣' in title:
        rc = RECT()
        u32.GetWindowRect(hwnd, ctypes.byref(rc))
        w = rc.right - rc.left
        h = rc.bottom - rc.top
        print(f"Evaluating 直播伴侣 {hwnd}: {w}x{h}")
        if w > 500 and h > 400:
            # Capture using BitBlt from screen DC directly
            hdcScreen = u32.GetDC(0)
            hdcMem = g32.CreateCompatibleDC(hdcScreen)
            hBitmap = g32.CreateCompatibleBitmap(hdcScreen, w, h)
            g32.SelectObject(hdcMem, hBitmap)
            
            # BitBlt from screen coordinates
            SRCCOPY = 0x00CC0020
            res = g32.BitBlt(hdcMem, 0, 0, w, h, hdcScreen, rc.left, rc.top, SRCCOPY)
            print("BitBlt result:", res)
            
            # Save as BMP
            import win32ui
            saveBitMap = win32ui.CreateBitmapFromHandle(hBitmap)
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
            save_path = r'C:\Users\林夏\.gemini\antigravity-cli\brain\ca7952b9-cf9e-4d43-83dc-3bdc35eccb54\companion_real_window.png'
            im.save(save_path)
            print("SAVED COMPANION SCREENSHOT TO:", save_path)
            
            g32.DeleteDC(hdcMem)
            u32.ReleaseDC(0, hdcScreen)
            break
