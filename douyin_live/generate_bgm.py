import os
import math
import struct
import wave
import numpy as np

os.makedirs(r'D:\zhibo\Open-LLM-VTuber\douyin_live\music', exist_ok=True)

def generate_track(filename, chords, tempo=105, instrument='marimba'):
    sample_rate = 44100
    beat_dur = 60.0 / tempo
    total_beats = len(chords) * 4
    total_samples = int(total_beats * beat_dur * sample_rate)
    buffer = np.zeros(total_samples, dtype=float)
    
    # Note frequencies (Hz)
    note_freqs = {
        'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61, 'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
        'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
        'C6': 1046.50
    }
    
    def add_note(note, start_beat, duration_beats, volume=0.25):
        if note not in note_freqs:
            return
        freq = note_freqs[note]
        start_sample = int(start_beat * beat_dur * sample_rate)
        dur_samples = int(duration_beats * beat_dur * sample_rate)
        if start_sample >= total_samples:
            return
        actual_samples = min(dur_samples, total_samples - start_sample)
        t = np.linspace(0, actual_samples / sample_rate, actual_samples, endpoint=False)
        
        # Envelope: soft attack, exponential decay (bell/marimba sound)
        if instrument == 'marimba':
            env = np.exp(-t * 3.5) * (1.0 - np.exp(-t * 80.0))
            wave_data = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2.0 * t) + 0.1 * np.sin(2 * np.pi * freq * 3.0 * t)
        else: # musicbox
            env = np.exp(-t * 2.2) * (1.0 - np.exp(-t * 120.0))
            wave_data = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 2.0 * t) + 0.25 * np.sin(2 * np.pi * freq * 4.0 * t)
            
        note_audio = wave_data * env * volume
        buffer[start_sample:start_sample + actual_samples] += note_audio

    # Compose rhythmic pattern based on chords
    current_beat = 0
    for chord in chords:
        # Bass note on beat 1 and 3
        bass = chord[0]
        add_note(bass, current_beat, 1.8, volume=0.22)
        add_note(bass, current_beat + 2, 1.8, volume=0.18)
        
        # Arpeggios on beats 1, 2, 3, 4
        add_note(chord[1], current_beat, 0.8, volume=0.15)
        add_note(chord[2], current_beat + 1, 0.8, volume=0.16)
        add_note(chord[3], current_beat + 2, 0.8, volume=0.18)
        add_note(chord[2], current_beat + 3, 0.8, volume=0.15)
        
        # Melody on top
        if len(chord) > 4:
            add_note(chord[4], current_beat + 0.5, 1.2, volume=0.16)
            add_note(chord[3], current_beat + 2.5, 1.2, volume=0.14)
            
        current_beat += 4

    # Normalize audio
    max_val = np.max(np.abs(buffer))
    if max_val > 0:
        buffer = buffer / max_val * 0.75

    # Write WAV file
    out_path = os.path.join(r'D:\zhibo\Open-LLM-VTuber\douyin_live\music', filename)
    with wave.open(out_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        # convert to 16-bit PCM
        int16_data = (buffer * 32767).astype(np.int16)
        wf.writeframes(int16_data.tobytes())
    print(f"Generated {out_path} ({len(buffer)/sample_rate:.1f}s)")

# Track 1: Happy Chibi Marimba (C - G - Am - F progression, light & joyful)
generate_track(
    'happy_chibi_bgm.wav',
    [
        ['C3', 'E4', 'G4', 'C5', 'E5'],
        ['G3', 'D4', 'G4', 'B4', 'D5'],
        ['A3', 'C4', 'E4', 'A4', 'C5'],
        ['F3', 'C4', 'F4', 'A4', 'C5'],
        ['C3', 'E4', 'G4', 'C5', 'G5'],
        ['G3', 'D4', 'G4', 'B4', 'E5'],
        ['A3', 'C4', 'E4', 'A4', 'D5'],
        ['F3', 'A4', 'C5', 'F5', 'C5']
    ],
    tempo=108,
    instrument='marimba'
)

# Track 2: Sweet Lullaby Music Box (Warm, cozy, soothing for 奶娃)
generate_track(
    'sweet_lullaby_bgm.wav',
    [
        ['C3', 'G4', 'C5', 'E5', 'G5'],
        ['F3', 'A4', 'C5', 'F5', 'A5'],
        ['G3', 'B4', 'D5', 'G5', 'B5'],
        ['C3', 'E4', 'G4', 'C5', 'E5'],
        ['A3', 'E4', 'A4', 'C5', 'E5'],
        ['D3', 'F4', 'A4', 'D5', 'F5'],
        ['G3', 'D4', 'G4', 'B4', 'D5'],
        ['C3', 'G4', 'C5', 'E5', 'C6']
    ],
    tempo=88,
    instrument='musicbox'
)
