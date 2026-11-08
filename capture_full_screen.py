# -*- coding: utf-8 -*-
import ctypes
from PIL import Image

u32 = ctypes.windll.user32
g32 = ctypes.windll.gdi32

input_desk = u32.OpenInputDesktop(0, False, 0x01FF)
u32.SetThreadDesktop(input_desk)

w = u32.GetSystemMetrics(0) # SM_CXSCREEN
h = u32.GetSystemMetrics(1) # SM_CYSCREEN
print(f"Screen resolution: {w}x{h}")

hdcScreen = u32.GetDC(0)
hdcMem = g32.CreateCompatibleDC(hdcScreen)
hBitmap = g32.CreateCompatibleBitmap(hdcScreen, w, h)
g32.SelectObject(hdcMem, hBitmap)

SRCCOPY = 0x00CC0020
res = g32.BitBlt(hdcMem, 0, 0, w, h, hdcScreen, 0, 0, SRCCOPY)
print("BitBlt screen result:", res)

import win32ui
saveBitMap = win32ui.CreateBitmapFromHandle(hBitmap)
bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)
im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
save_path = r'C:\Users\林夏\.gemini\antigravity-cli\brain\ca7952b9-cf9e-4d43-83dc-3bdc35eccb54\full_desktop_screen.png'
im.save(save_path)
print("SAVED FULL DESKTOP SCREENSHOT TO:", save_path)

g32.DeleteDC(hdcMem)
u32.ReleaseDC(0, hdcScreen)
