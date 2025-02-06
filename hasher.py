from spectrogram import PointMarker


# anonymous hash, contains details about a pair of points
class Hash():

    def __init__(self, anchor_freq, pair_freq, time_delta, anchor_time_abs):
        self.anchor_freq = anchor_freq
        self.pair_freq = pair_freq
        self.time_delta = time_delta
        self.anchor_time_abs = anchor_time_abs

    def __hash__(self):
        return hash((self.anchor_freq, self.pair_freq, self.time_delta))


class Hasher():

    def __init__(self, spectral_peaks):
        self.spectral_peaks = spectral_peaks

        # default anchor point target zone parameters
        self.t_offset = 0.2 # points before anchor time + t_offset will not be considered
        self.t_size = 4 # points after anchor time + t_offset + t_size will not be considered
        self.freq_spread = 1000 # points bellow anchor freq - freq_spread or above anchor freq + freq_spread will not be considered

    def generate_hashes(self, all_anchors=True, group_by_anchors=False):

        anchor_points = []

        if all_anchors:
            anchor_points = self.spectral_peaks
        else:
            raise NotImplementedError

        hashes = []

        for anchor_point in self.spectral_peaks:

            if group_by_anchors:
                hashes.append([])

            for point in self.spectral_peaks:

                # cases where point isn't in target zone of anchor point
                if point.time < anchor_point.time + self.t_offset:
                    continue
                if point.time > anchor_point.time + self.t_offset + self.t_size:
                    continue
                if point.freq < anchor_point.freq - self.freq_spread:
                    continue
                if point.freq > anchor_point.freq + self.freq_spread:
                    continue
                
                time_delta = anchor_point.time - anchor_point.time
                new_hash = Hash(anchor_point.freq, point.freq, time_delta, anchor_point.time)

                if group_by_anchors:
                    hashes[-1].append(new_hash)
                else:
                    hashes.append(new_hash)

        return hashes