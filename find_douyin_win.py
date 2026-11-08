# -*- coding: utf-8 -*-
import ctypes
import win32gui
import win32process

u32 = ctypes.windll.user32
input_desk = u32.OpenInputDesktop(0, False, 0x01FF)
u32.SetThreadDesktop(input_desk)

def cb(hwnd, extra):
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    title = win32gui.GetWindowText(hwnd)
    cls = win32gui.GetClassName(hwnd)
    vis = win32gui.IsWindowVisible(hwnd)
    if any(k in title for k in ['伴侣', '直播', '抖音']) or any(k in cls.lower() for k in ['douyin', 'webcast', 'chrome_widgetwin']):
        if title:
            print(f'HWND: {hwnd}, PID: {pid}, Vis: {vis}, Title: "{title}", Class: "{cls}"')

win32gui.EnumWindows(cb, None)
