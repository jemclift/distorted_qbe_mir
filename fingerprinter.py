from spectrogram import PointMarker
from itertools import product

class Fingerprinter():
    def __init__(self, spectrum, row_freqs, col_times):
        self.spectrum = spectrum
        self.row_freqs = row_freqs
        self.col_times = col_times

    # creates a constellation map of spectral peaks
    def find_peaks(self):

        peaks = []

        for row_i, sg_row in enumerate(self.spectrum):
            for col_i, sg_item in enumerate(sg_row):

                #    a
                # d  +  b
                #    c

                a, b, c, d = 7, 25, 7, 25

                if self.is_local_maxima((row_i, col_i), (a, b, c, d)):
                    peak = PointMarker(self.col_times[col_i], self.row_freqs[row_i])
                    peaks.append(peak)

            print(f"{row_i+1} / {self.spectrum.shape[0]}")

        input(len(peaks))

        return peaks


    def pixel_energy(self, coord):
        
        y, x = coord
        return self.row_freqs[y] * self.spectrum[y, x]


    def is_local_maxima(self, center, kernel_spans):

        c_y, c_x = center
        a, b, c, d = kernel_spans
        center_value = self.spectrum[c_y, c_x]
        center_energy = self.pixel_energy((c_y, c_x))

        for y in range(c_y - a, c_y + c + 1):
            # out of bounds
            if y < 0 or y >= self.spectrum.shape[0]:
                continue

            for x in range(c_x - d, c_x + b + 1):
                # out of bounds
                if x < 0 or x >= self.spectrum.shape[1]:
                    continue

                # centre pixel
                if y == c_y and x == c_x:
                    continue

                if self.spectrum[y, x] >= center_value or self.pixel_energy((y, x)) >= center_energy:
                    return False

        return True