import os

path = r'D:\zhibo\Open-LLM-VTuber\douyin_live\index.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

replacements = [
    ('✦ 小黄呆呆球 ✦', '✦ 软糖小主播 · 奶娃 ✦'),
    ('呼……本球正在发呆，快发弹幕或喂我吃白饭吧！', '咕噜咕噜……奶娃肚子里在打小鼓鼓，想吃香喷喷的甜甜饭饭啦～'),
    ("setSpeech('好耶！本球给你表演一个原地高弹跳！收到！');", "setSpeech('好耶好耶！谢谢哥哥姐姐，奶娃给你表演个软糖跳！duang duang~');"),
    ("setSpeech('咕噜噜……看我吹出一个无敌七彩大泡泡！');", "setSpeech('咕噜咕噜……奶娃吹大泡泡啦！大泡泡要飞到哥哥姐姐鼻尖上啦！');"),
    ("setSpeech('呼……好困呀，谁也不准吵我睡觉觉……Zzz');", "setSpeech('呼噜呼噜……奶娃眼睛打架了，要睡饱饱觉觉啦……Zzz');"),
    ("setSpeech('嗷呜！是谁砸我！直接给本球干成荷包蛋煎饼了！');", "setSpeech('哎呀呀！奶娃被压成软糖煎饼啦！不过奶娃马上弹回来，duang~！');"),
    ("setSpeech('嗝~~ 吃太饱了！本球已经变成一个充气大气球啦！');", "setSpeech('吧唧吧唧……奶娃肚肚吃得圆滚滚像大皮球啦，饱饱！');"),
    ("setSpeech('哎呀呀~ 你们这么夸我，人家小脸都要红透了啦！');", "setSpeech('呜哇～哥哥姐姐夸奶娃，奶娃小脸热热的，腮红红透啦！');"),
    ("setSpeech('动起来！跟着节拍扭扭扭，看谁屁股扭得圆！');", "setSpeech('一摇一摆～奶娃扭扭扭，和哥哥姐姐一起快乐贴贴！');"),
    ("setSpeech('哇啊啊！吓死本球了，小心脏扑通扑通跳！');", "setSpeech('咦？奶娃还小，脑袋里全是糊糊，不懂耶～');"),
    ("setSpeech('哇！满屏都是爱心瀑布！我要被爱意淹没啦！');", "setSpeech('哇！满屏都是甜甜小心心！奶娃要和哥哥姐姐抱抱！');"),
    ("setSpeech('感谢大哥的豪华暴击！全体起立！今晚本球宣布全场开荤！');", "setSpeech('哇啊！大闪闪！谢谢哥哥姐姐，奶娃超级开心，duang duang弹跳！');"),
    ("startTalking('问我爸是谁干嘛，你就没点别的好奇心？本球可是宇宙第一可爱小奶球！');", "startTalking('哥哥姐姐好呀！奶娃三岁半啦，说话是肚肚咕噜咕噜发出来的哦～');")
]

for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
    else:
        print("Not found:", old)

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
