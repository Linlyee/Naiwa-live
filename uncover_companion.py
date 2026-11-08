# -*- coding: utf-8 -*-
import ctypes
import time
from PIL import Image

u32 = ctypes.windll.user32
g32 = ctypes.windll.gdi32

input_desk = u32.OpenInputDesktop(0, False, 0x01FF)
u32.SetThreadDesktop(input_desk)

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

companion_hwnd = None

def cb(hwnd, lParam):
    global companion_hwnd
    length = u32.GetWindowTextLengthW(hwnd)
    if length > 0:
        buf = ctypes.create_unicode_buffer(length + 1)
        u32.GetWindowTextW(hwnd, buf, length + 1)
        title = buf.value
        cls_buf = ctypes.create_unicode_buffer(256)
        u32.GetClassNameW(hwnd, cls_buf, 256)
        cls = cls_buf.value
        if u32.IsWindowVisible(hwnd):
            if 'PowerShell' in title or '弹幕' in title or 'Barrage' in title:
                # Minimize covering windows
                u32.ShowWindow(hwnd, 6) # SW_MINIMIZE
                print(f"Minimized {title}")
            elif '直播伴侣' in title and 'Chrome_WidgetWin' in cls:
                companion_hwnd = hwnd
    return True

u32.EnumDesktopWindows(input_desk, WNDENUMPROC(cb), 0)

if companion_hwnd:
    print(f"Found companion HWND: {companion_hwnd}")
    u32.ShowWindow(companion_hwnd, 9) # SW_RESTORE
    u32.SetForegroundWindow(companion_hwnd)
    time.sleep(1)

w = u32.GetSystemMetrics(0)
h = u32.GetSystemMetrics(1)
hdcScreen = u32.GetDC(0)
hdcMem = g32.CreateCompatibleDC(hdcScreen)
hBitmap = g32.CreateCompatibleBitmap(hdcScreen, w, h)
g32.SelectObject(hdcMem, hBitmap)
SRCCOPY = 0x00CC0020
g32.BitBlt(hdcMem, 0, 0, w, h, hdcScreen, 0, 0, SRCCOPY)

import win32ui
saveBitMap = win32ui.CreateBitmapFromHandle(hBitmap)
bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)
im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
save_path = r'C:\Users\林夏\.gemini\antigravity-cli\brain\ca7952b9-cf9e-4d43-83dc-3bdc35eccb54\companion_uncovered.png'
im.save(save_path)
print("Saved uncovered companion screenshot to:", save_path)

g32.DeleteDC(hdcMem)
u32.ReleaseDC(0, hdcScreen)
