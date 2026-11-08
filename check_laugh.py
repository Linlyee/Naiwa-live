import imageio_ffmpeg
import subprocess

exe = imageio_ffmpeg.get_ffmpeg_exe()

cmd = [exe, '-i', 'nailong_audio.mp3', '-af', 'silencedetect=noise=-30dB:d=0.3', '-f', 'null', '-']
res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
for line in res.stderr.splitlines():
    if 'silence_' in line:
        print(line)
