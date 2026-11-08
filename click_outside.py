# -*- coding: utf-8 -*-
import ctypes, time

u32 = ctypes.windll.user32
input_desk = u32.OpenInputDesktop(0, False, 0x01FF)
u32.SetThreadDesktop(input_desk)

x = 500
y = 200
u32.SetCursorPos(x, y)
time.sleep(0.1)
# MOUSEEVENTF_LEFTDOWN = 0x0002, MOUSEEVENTF_LEFTUP = 0x0004
u32.mouse_event(0x0002, 0, 0, 0, 0)
time.sleep(0.05)
u32.mouse_event(0x0004, 0, 0, 0, 0)
print(f"Clicked at ({x}, {y})")
