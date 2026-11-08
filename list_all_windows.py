# -*- coding: utf-8 -*-
import uiautomation as auto

print("Listing all visible top-level windows:")
for win in auto.GetRootControl().GetChildren():
    try:
        if win.IsOffscreen:
            continue
        print(f"Name='{win.Name}', Class='{win.ClassName}', BoundingRect={win.BoundingRectangle}")
    except:
        pass
