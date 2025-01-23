from spectrogram import PointMarker

class Fingerprinter():
    def __init__(self, spectrogram):
        self.spectrogram = spectrogram

    # creates a constellation map of spectral peaks
    def choose_peaks(self):
        return [PointMarker(40, 8_000), PointMarker(60, 10_000), PointMarker(80, 12_000)]



# using spectrogram peaks

# A time-frequency point is a candidate peak if:

# - it has a higher energy content than all its neighbours in a region centered around the point.
# (energy is a product of amplitude and frequency)

# - Candidate peaks are chosen according to a density criterion in order to assure that the time-frequency strip for the audio file has reasonably uniform coverage.

# - The peaks in each time-frequency locality are also chosen according amplitude, with the justification that the highest amplitude peaks are most likely to survive the distortions listed above.