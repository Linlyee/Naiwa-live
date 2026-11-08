import os
import wave
import pyttsx3

VOICE_DIR = 'douyin_live/assets/voice'
os.makedirs(VOICE_DIR, exist_ok=True)

engine = pyttsx3.init()
engine.setProperty('rate', 155)
engine.setProperty('volume', 1.0)

voices = engine.getProperty('voices')
for v in voices:
    if 'zh' in v.id.lower() or 'chinese' in v.name.lower() or 'huihui' in v.name.lower():
        engine.setProperty('voice', v.id)
        print("Using voice:", v.name)
        break

clips = {
    'intro': "哥哥姐姐好呀！我是小主播奶娃，说话是肚子里咕噜咕噜发出来的哦～",
    'boing': "好耶好耶！谢谢哥哥姐姐，奶娃给你表演个软糖跳！duang duang~",
    'bubbles': "咕噜咕噜……奶娃吹大泡泡啦！大泡泡要飞到哥哥姐姐鼻尖上啦！",
    'sleep': "呼噜呼噜……奶娃眼睛打架了，要睡饱饱觉觉啦……",
    'squish': "哎呀呀！奶娃被压成软糖煎饼啦！不过奶娃马上弹回来，duang~！",
    'bloat': "吧唧吧唧……奶娃肚肚吃得圆滚滚像大皮球啦，饱饱！",
    'blush': "呜哇～哥哥姐姐夸奶娃，奶娃小脸热热的，腮红红透啦！",
    'dance': "一摇一摆～奶娃扭扭扭，和哥哥姐姐一起快乐贴贴！",
    'shiver': "咦？奶娃还小，脑袋里全是糊糊，不懂耶～",
    'hearts': "哇！满屏都是甜甜小心心！奶娃要和哥哥姐姐抱抱！",
    'gold': "哇啊！大闪闪！谢谢哥哥姐姐，奶娃超级开心，duang duang弹跳！",
    'hungry': "咕噜噜……奶娃饿扁啦，脑袋全是糊糊，求哥哥姐姐投喂一口饭饭嘛～",
    'revive': "哇！香喷喷的饭饭！奶娃满血复活啦，duang duang~",
    'song': "好听好听！这首歌排上啦，马上给哥哥姐姐放～"
}

for name, text in clips.items():
    raw_path = os.path.join(VOICE_DIR, f"raw_{name}.wav")
    final_path = os.path.join(VOICE_DIR, f"{name}.wav")
    
    engine.save_to_file(text, raw_path)
    engine.runAndWait()
    
    # Apply 1.25x cute child pitch shift
    if os.path.exists(raw_path):
        with wave.open(raw_path, 'rb') as wf:
            params = wf.getparams()
            frames = wf.readframes(wf.getnframes())
        
        new_rate = int(params.framerate * 1.24)
        with wave.open(final_path, 'wb') as wf:
            wf.setparams((params.nchannels, params.sampwidth, new_rate, params.nframes, params.comptype, params.compname))
            wf.writeframes(frames)
        
        os.remove(raw_path)
        print(f"Generated {final_path} ({os.path.getsize(final_path)} bytes)")

print("All cute voice clips generated successfully!")
