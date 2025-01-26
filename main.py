from audio import Audio
from spectrogram import Spectrogram, PointMarker
from fingerprinter import Fingerprinter

tcr = Audio("The Clocktower Reel.wav", 1)

tcr_spg = Spectrogram(tcr.audio_data, tcr.sampling_freq)
tcr_fp = Fingerprinter(tcr_spg.spectrum, tcr_spg.row_freqs, tcr_spg.col_times)

for pm in tcr_fp.find_peaks():
    tcr_spg.add_point_marker(pm)

tcr_spg.display()