# -*- coding: utf-8 -*-
import ctypes
import uiautomation as auto

u32 = ctypes.windll.user32
input_desk = u32.OpenInputDesktop(0, False, 0x01FF)
u32.SetThreadDesktop(input_desk)

dlg = auto.ControlFromHandle(1248088)
print("Dialog Name:", dlg.Name)

# Find all buttons
for b in dlg.GetChildren():
    print(f"Child: [{b.ControlTypeName}] '{b.Name}', rect: {b.BoundingRectangle}")
    for c in b.GetChildren():
        print(f"  Grandchild: [{c.ControlTypeName}] '{c.Name}', rect: {c.BoundingRectangle}")
