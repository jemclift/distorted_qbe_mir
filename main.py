from audio import Audio
from spectrogram import Spectrogram, PointMarker
from fingerprinter import Fingerprinter

tcr = Audio("The Clocktower Reel.wav", 1)

tcr_spg = Spectrogram(tcr.audio_data, tcr.sampling_freq)
tcr_fp = Fingerprinter(tcr_spg)

for pm in tcr_fp.choose_peaks():
    tcr_spg.add_point_marker(pm)

tcr_spg.display()