# -*- coding: utf-8 -*-
import ctypes
import uiautomation as auto

u32 = ctypes.windll.user32
input_desk = u32.OpenInputDesktop(0, False, 0x01FF)
u32.SetThreadDesktop(input_desk)

hwnd = 1248088
ctrl = auto.ControlFromHandle(hwnd)
print("Root control for 直播伴侣:", ctrl.Name, ctrl.ClassName)

def dump_controls(c, depth=0):
    if depth > 4:
        return
    for child in c.GetChildren():
        try:
            name = child.Name
            c_type = child.ControlTypeName
            rect = child.BoundingRectangle
            if name:
                print("  " * depth + f"[{c_type}] {name} (Rect: {rect})")
            dump_controls(child, depth + 1)
        except:
            pass

dump_controls(ctrl)
