# -*- coding: utf-8 -*-
import ctypes
import win32gui
import win32process

u32 = ctypes.windll.user32
input_desk = u32.OpenInputDesktop(0, False, 0x01FF)
u32.SetThreadDesktop(input_desk)

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

edge_hwnd = None
def cb(hwnd, lParam):
    global edge_hwnd
    title = win32gui.GetWindowText(hwnd)
    cls = win32gui.GetClassName(hwnd)
    vis = win32gui.IsWindowVisible(hwnd)
    if 'Chrome_WidgetWin_1' in cls:
        rect = win32gui.GetWindowRect(hwnd)
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]
        print(f"HWND {hwnd}: w={w}, h={h}, title='{title}'")
        if w < 700 and h > 800:
            edge_hwnd = hwnd
    return True

u32.EnumDesktopWindows(input_desk, WNDENUMPROC(cb), 0)

if edge_hwnd:
    print(f"Bringing Edge window {edge_hwnd} to foreground!")
    u32.ShowWindow(edge_hwnd, 9)
    u32.SetForegroundWindow(edge_hwnd)
    # Position it nicely on the right side of the screen
    u32.SetWindowPos(edge_hwnd, 0, 1100, 20, 576, 1024, 0x0040)
