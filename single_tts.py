import sys
import os
import urllib.request
import json
import subprocess

DEFAULT_VOICE = "speech:nailong_pure_crystal:d80vfqecnncc73bibn1g:zawoltqvcsospxihbsdn"
SILICON_API_KEY = os.environ.get("SILICONFLOW_API_KEY", "your-siliconflow-api-key")
SILICON_URL = "https://api.siliconflow.cn/v1/audio/speech"

def generate_speech(text: str, out_path: str, voice: str = DEFAULT_VOICE, timeout: int = 10) -> bool:
    """合成高保真 MP3 语音并经录音棚母带降噪与防削波（去电流/去破音/去金属杂音）"""
    text = text.strip()
    if not text:
        return False

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)

    data = {
        'model': 'FunAudioLLM/CosyVoice2-0.5B',
        'input': text,
        'voice': voice,
        'response_format': 'mp3',
        'sample_rate': 32000,
        'speed': 1.0
    }

    req = urllib.request.Request(
        SILICON_URL,
        data=json.dumps(data).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {SILICON_API_KEY}',
            'Content-Type': 'application/json'
        }
    )

    raw_tmp = out_path + f".raw.{os.getpid()}.mp3"
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read()
            if content and len(content) > 100:
                with open(raw_tmp, 'wb') as f:
                    f.write(content)

                # 母带级声学净化流水线：
                # 1. highpass=f=60: 滤除工频 50Hz/60Hz 底噪电流嗡嗡声
                # 2. lowpass=f=7200: 滤除神经声码器高频金属嘶嘶杂音 (Vocoder Sizzle)
                # 3. volume=0.78: 提供 2.5dB 充足动态余量，杜绝数字削波撞顶失真 (Anti-Clipping)
                # 4. -ar 44100 -ac 2: 转为标准 44.1kHz 双声道，与声卡/直播系统原生对齐，杜绝重采样插值破音
                try:
                    import imageio_ffmpeg
                    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                    cmd = [
                        ffmpeg_exe, '-i', raw_tmp,
                        '-af', 'volume=0.78,lowpass=f=7200,highpass=f=60',
                        '-ar', '44100', '-ac', '2', '-b:a', '192k',
                        out_path, '-y'
                    ]
                    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    if res.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 100:
                        if os.path.exists(raw_tmp):
                            try:
                                os.remove(raw_tmp)
                            except Exception:
                                pass
                        return True
                except Exception as ef:
                    print(f"[Mastering Warning] {ef}", file=sys.stderr)

                # 回退方案
                if os.path.exists(out_path):
                    try:
                        os.remove(out_path)
                    except Exception:
                        pass
                os.replace(raw_tmp, out_path)
                return True
    except Exception as e:
        print(f"[TTS Error] {e}", file=sys.stderr)
        if os.path.exists(raw_tmp):
            try:
                os.remove(raw_tmp)
            except Exception:
                pass
        return False

    return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python single_tts.py <text> <out_path> [voice]", file=sys.stderr)
        sys.exit(1)

    t = sys.argv[1]
    o = sys.argv[2]
    v = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_VOICE

    ok = generate_speech(t, o, v)
    if ok:
        print(f"Generated {o} ({os.path.getsize(o)} bytes) [Voice: {v}]")
        sys.exit(0)
    else:
        sys.exit(1)
