from audio import Audio
from spectrogram import Spectrogram, PointMarker
from fingerprinter import Fingerprinter

# load the audio, spectrogram and fingerprinter
tcr = Audio("The Clocktower Reel.wav", 1)
tcr_spg = Spectrogram(tcr.audio_data, tcr.sampling_freq)
tcr_fp = Fingerprinter(tcr_spg.spectrum, tcr_spg.row_freqs, tcr_spg.col_times)

# limit the search and display axis
freq_range = (0, 4000)
time_range = (4, 18)

# find the spectral peaks and add their point markers to the graph
for pm in tcr_fp.find_peaks(*freq_range, *time_range):
    tcr_spg.add_point_marker(pm)

tcr_spg.display(*freq_range, *time_range, False)