import numpy as np
import matplotlib.pyplot as plt


class PointMarker():

    def __init__(self, time, freq):
        self.time = time
        self.freq = freq


class Spectrogram():

    def __init__(self, audio_data, sampling_freq):

        # input audio
        self.audio_data = audio_data
        self.sampling_freq = sampling_freq

        # spectrogram
        self.spectrum = 0
        self.row_freqs = 0
        self.col_times = 0
        self.calculate_spectrogram()

        # scatter overlay
        self.point_marker_xs = []
        self.point_marker_ys = []


    def calculate_spectrogram(self):

        self.spectrum, self.row_freqs, self.col_times, _ = plt.specgram(
            self.audio_data, 
            NFFT=1024, 
            Fs=self.sampling_freq, 
            scale="dB")

        plt.close()


    def add_point_marker(self, point_marker):

        self.point_marker_xs.append(point_marker.time)
        self.point_marker_ys.append(point_marker.freq)


    def display(self, limit_freq=None, spg=True):

        fig, ax = plt.subplots(figsize=(12, 6))
        # fig, ax = plt.subplots()

        if limit_freq:
            ax.set_ylim(*limit_freq)

        if spg:
            plt.pcolormesh(
                self.col_times, 
                self.row_freqs, 
                10 * np.log10(self.spectrum), # convert intensity to dB
                # cmap='gray',
                shading='auto')

            plt.colorbar(label="intensity (dB)")

        plt.title("spectrogram")
        plt.xlabel("time (s)")
        plt.ylabel("frequency (Hz)")

        plt.scatter(self.point_marker_xs, self.point_marker_ys, c="k", marker="x")

        plt.show(block=False)

        input("press enter to close plot...")
        plt.close()
