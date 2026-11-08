# -*- coding: utf-8 -*-
import uiautomation as auto

print("Scanning top-level windows...")
for win in auto.GetRootControl().GetChildren():
    name = win.Name
    class_name = win.ClassName
    try:
        if any(k in name for k in ['伴侣', '直播', 'douyin', '抖音']) or 'webcast' in class_name.lower():
            print(f'Found: Name="{name}", Class="{class_name}", Handle={win.NativeWindowHandle}')
    except Exception as e:
        pass
print("Scan done.")
