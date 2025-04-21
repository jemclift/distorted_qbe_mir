from spectrogram import PointMarker


# anonymous hash, contains details about a pair of points
class Hash():

    def __init__(self, time_delta_1, freq_delta_1, time_delta_2, freq_delta_2, anchor_time_abs):
        self.time_delta_1 = time_delta_1
        self.freq_delta_1 = freq_delta_1
        self.time_delta_2 = time_delta_2
        self.freq_delta_2 = freq_delta_2
        self.anchor_time_abs = anchor_time_abs

    def __hash__(self):
        return hash((self.time_delta_1, self.freq_delta_1, self.time_delta_2, self.freq_delta_2))


class Hasher():

    def __init__(self, spectral_peaks):
        self.spectral_peaks = spectral_peaks

        # default anchor point target zone parameters
        # self.t_offset = 0.2 # points before anchor time + t_offset will not be considered
        # self.t_size = 4 # points after anchor time + t_offset + t_size will not be considered
        # self.freq_spread = 1000 # points bellow anchor freq - freq_spread or above anchor freq + freq_spread will not be considered

        self.t_offset = 0
        self.t_size = 4
        self.freq_spread = 1000


    def get_target_zone_points(self, anchor):

        points = []

        for point in self.spectral_peaks:

            # cases where point isn't in target zone of anchor point
            if point.time < anchor.time + self.t_offset:
                continue
            if point.time > anchor.time + self.t_offset + self.t_size:
                continue
            if point.freq < anchor.freq - self.freq_spread:
                continue
            if point.freq > anchor.freq + self.freq_spread:
                continue

            points.append(point)

        return points


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

            target_points = self.get_target_zone_points(anchor_point)

            for point_1 in target_points:
                for point_2 in target_points:

                    if point_1 != point_2:
                
                        time_delta_1 = point_1.time - anchor_point.time
                        freq_delta_1 = point_1.freq - anchor_point.freq

                        time_delta_2 = point_2.time - anchor_point.time
                        freq_delta_2 = point_2.freq - anchor_point.freq

                        # time_delta_1 = point_1.time - anchor_point.time
                        # freq_delta_1 = point_1.freq - anchor_point.freq

                        # time_delta_2 = point_2.time - point_1.time
                        # freq_delta_2 = point_2.freq - point_1.freq

                        new_hash = Hash(time_delta_1, freq_delta_1, time_delta_2, freq_delta_2, anchor_point.time)

                        if group_by_anchors:
                            hashes[-1].append(new_hash)
                        else:
                            hashes.append(new_hash)

        return hashes