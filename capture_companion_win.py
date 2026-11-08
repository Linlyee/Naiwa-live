# -*- coding: utf-8 -*-
import ctypes
import win32gui
import win32ui
import win32con
import win32process
from PIL import Image

u32 = ctypes.windll.user32
input_desk = u32.OpenInputDesktop(0, False, 0x01FF)
u32.SetThreadDesktop(input_desk)

target_hwnd = None
def cb(hwnd, extra):
    global target_hwnd
    title = win32gui.GetWindowText(hwnd)
    cls = win32gui.GetClassName(hwnd)
    vis = win32gui.IsWindowVisible(hwnd)
    if '直播伴侣' in title and vis and 'Chrome_WidgetWin' in cls:
        rect = win32gui.GetWindowRect(hwnd)
        if (rect[2] - rect[0]) > 400: # Main window
            target_hwnd = hwnd
            print(f"Found main companion window: HWND {hwnd}, size {rect[2]-rect[0]}x{rect[3]-rect[1]}")

win32gui.EnumWindows(cb, None)

if target_hwnd:
    rect = win32gui.GetWindowRect(target_hwnd)
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]
    
    hwndDC = win32gui.GetWindowDC(target_hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)

    res = u32.PrintWindow(target_hwnd, saveDC.GetSafeHdc(), 2)
    print("PrintWindow res:", res)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(target_hwnd, hwndDC)
    win32gui.DeleteObject(saveBitMap.GetHandle())

    save_path = r'C:\Users\林夏\.gemini\antigravity-cli\brain\ca7952b9-cf9e-4d43-83dc-3bdc35eccb54\companion_real_window.png'
    im.save(save_path)
    print("Saved companion screenshot successfully to:", save_path)
else:
    print("Target window not found.")
