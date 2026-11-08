# -*- coding: utf-8 -*-
import ctypes
import win32gui
import win32process

u32 = ctypes.windll.user32
input_desk = u32.OpenInputDesktop(0, False, 0x01FF)
u32.SetThreadDesktop(input_desk)

def cb(hwnd, extra):
    title = win32gui.GetWindowText(hwnd)
    cls = win32gui.GetClassName(hwnd)
    vis = win32gui.IsWindowVisible(hwnd)
    if 'msedge' in cls.lower() or 'chrome' in cls.lower() or '抖音' in title or '奶娃' in title or 'localhost' in title:
        rect = win32gui.GetWindowRect(hwnd)
        print(f"HWND: {hwnd}, Vis: {vis}, Title: '{title}', Rect: {rect}")

win32gui.EnumWindows(cb, None)
