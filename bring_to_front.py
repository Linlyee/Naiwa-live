# -*- coding: utf-8 -*-
import ctypes
import time
from PIL import Image

u32 = ctypes.windll.user32
g32 = ctypes.windll.gdi32

input_desk = u32.OpenInputDesktop(0, False, 0x01FF)
u32.SetThreadDesktop(input_desk)

hwnd = 1248088
print("Bringing 直播伴侣 to foreground...")
u32.ShowWindow(hwnd, 9) # SW_RESTORE
u32.SetForegroundWindow(hwnd)
time.sleep(1)

# Capture screen
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
save_path = r'C:\Users\林夏\.gemini\antigravity-cli\brain\ca7952b9-cf9e-4d43-83dc-3bdc35eccb54\companion_foreground.png'
im.save(save_path)
print("Saved companion foreground screenshot to:", save_path)

g32.DeleteDC(hdcMem)
u32.ReleaseDC(0, hdcScreen)
