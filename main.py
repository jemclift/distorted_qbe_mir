import wave
import numpy as np
import matplotlib.pyplot as plt

filename = "The Clocktower Reel.wav"

with wave.open(filename, "rb") as sound_file:

    assert sound_file.getsampwidth() == 2, "only 16 bit audio supported"

    channels = sound_file.getnchannels()  # audio channels (1 for mono, 2 for stereo)
    framerate = sound_file.getframerate()  # sampling frequency

    raw_data = sound_file.readframes(-1) # read all frames as bytes

audio_data = np.frombuffer(raw_data, dtype=np.int16)

if channels == 2:
    audio_data = audio_data[::2]  # take only one channel (left or right)

plt.figure(figsize=(12, 6))
plt.specgram(audio_data, NFFT=1024, Fs=framerate, scale="dB")

plt.xlabel("time (s)")
plt.ylabel("frequency (Hz)")
plt.colorbar(label="intensity (dB)")

plt.show()
