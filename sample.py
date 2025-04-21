from audio import Audio
from spectrogram import Spectrogram
from fingerprinter import Fingerprinter
from hasher import Hasher
from hough import Hough

import numpy as np
import matplotlib.pyplot as plt
import os


time_range = (None, None)
freq_range = (0, 5000)


class Sample():

    def __init__(self, filename, database, multiplier, load=True):

        self.filename = filename
        self.database = database
        self.multiplier = multiplier

        # can load manually if only spectral peaks are needed
        if load:
            self.load_stage_1()
            self.load_stage_2()


    # calculate spectrogram and spectral peaks
    def load_stage_1(self):

        self.audio = Audio(self.filename)
        self.spectrogram = Spectrogram(self.audio.audio_data, self.audio.sampling_freq)
        
        fingeprinter = Fingerprinter(self.spectrogram.spectrum, self.spectrogram.row_freqs, self.spectrogram.col_times)
        self.spectral_peaks = fingeprinter.find_peaks(*freq_range, *time_range)


    # create hashes and search in database
    def load_stage_2(self):

        hasher = Hasher(self.spectral_peaks)
        self.hashes = hasher.generate_hashes(True, True)
        
        self.song_hits = {}
        self.sample_time_per_track = {}
        self.database_time_per_track = {}

        self.catagorise_hashes()

    
    def show_peaks(self):

        for pm in self.spectral_peaks:
            self.spectrogram.add_point_marker(pm)

        self.spectrogram.display(freq_range)


    def store_hit(self, anchor_no, track_index, sample_offset, database_offset):

        if track_index not in self.sample_time_per_track:
            self.sample_time_per_track[track_index] = {}
            self.database_time_per_track[track_index] = {}

        if anchor_no not in self.sample_time_per_track[track_index]:
            self.sample_time_per_track[track_index][anchor_no] = []
            self.database_time_per_track[track_index][anchor_no] = []

        self.sample_time_per_track[track_index][anchor_no].append(sample_offset)
        self.database_time_per_track[track_index][anchor_no].append(database_offset)

        if track_index not in self.song_hits:
            self.song_hits[track_index] = 0

        self.song_hits[track_index] += 1


    def catagorise_hashes(self):
        for anchor_no, anchor_group in enumerate(self.hashes):

            for anon_hash in anchor_group:

                hits = self.database.search_hash(anon_hash)

                if hits == None:
                    continue

                for hit in hits:
                    track_index, database_offset = hit
                    self.store_hit(anchor_no, track_index, anon_hash.anchor_time_abs, database_offset)


    # adds reference line on y axis
    def reference_line_y(self, value, text, colour="k"):

        plt.axhline(value, color=colour)
        _, x_max = plt.gca().get_xlim()
        plt.text(x_max, value, f" {text}", color=colour, va='center')


    # looks through top track hash hits until a match is found (graphical version)
    def match_to_db_track_old(self):

        # start with track with most hash hits
        track_keys = sorted(self.song_hits.keys(), key=lambda k: self.song_hits[k], reverse=True)

        # collect std devs above mean, and tallest bars for later graph
        sd_a_means = {}
        tallest_bars = {}
        izzy_graph = {}

        for track in track_keys:

            # generate histogram

            offsets = []

            song_title = self.database.get_song_details(track).title

            # if song_title != "disco_00039.wav": continue
            # if song_title != "blues_00054.wav": continue
            # if song_title != "reggae_00063.wav": continue
            if song_title != "country_00025.wav": continue

            plt.figure(figsize=(12, 6))

            # all_xs = []
            # all_ys = []

            # for k in self.sample_time_per_track[track].keys():
            #     all_xs += self.database_time_per_track[track][k]
            #     all_ys += self.sample_time_per_track[track][k]

            # hough = Hough(all_xs, all_ys)
            # grad = hough.get_line_grad()
            # multiplier = 1/grad

            # print(f"actual {1.9295610185897200}")
            # print(f"calc   {multiplier}")

            for k in self.sample_time_per_track[track].keys():

                for s in range(len(self.database_time_per_track[track][k])):
                    # self.database_time_per_track[track][k][s] /= 1.83308297 # -5
                    # self.database_time_per_track[track][k][s] /= 1.88132199 # -2.5
                    # self.database_time_per_track[track][k][s] /= 1.91026541 # -1
                    self.database_time_per_track[track][k][s] /= 1.9295610185897200
                    # self.database_time_per_track[track][k][s] /= 1.94885663 # +1
                    # self.database_time_per_track[track][k][s] /= 1.97780004 # +2.5
                    # self.database_time_per_track[track][k][s] /= 2.02603907 # 5

                    # self.database_time_per_track[track][k][s] /= multiplier

                plt.scatter(self.database_time_per_track[track][k], self.sample_time_per_track[track][k], c="k", marker="x") # add c="k" for black

                for (d, s) in zip(self.database_time_per_track[track][k], self.sample_time_per_track[track][k]):
                    offsets.append(d - s)

            plt.title(f"track {track} ({song_title}) hash matches")
            plt.xlabel("database soundfile time")
            plt.ylabel("sample soundfile time")

            plt.show(block=False)
            input("press enter to close plot...")
            plt.close()

            counts, bins = np.histogram(offsets, bins=150)
            # counts, bins = np.histogram(offsets, bins=145)

            mean = np.mean(counts)
            std_dev = np.std(counts)
            tallest_bar = np.max(counts)
            sd_a_mean = (tallest_bar - mean) / std_dev
            median = np.median(counts)

            tallest_bars[track] = tallest_bar
            sd_a_means[track] = sd_a_mean
            izzy_graph[track] = sd_a_mean * sd_a_mean * tallest_bar

            # print(f"tallest bar {tallest_bar}")
            # print(f"track {track} - std. dev.s above mean {sd_a_mean}")

            # histogram of offsets
            plt.subplots(figsize=(12, 6))
            plt.stairs(counts, bins, color="#4D4670", fill=True)
            self.reference_line_y(mean, "mean")
            # self.reference_line_y(median, "median", colour="r")
            self.reference_line_y(mean + std_dev, "std. dev. above", colour="c")
            plt.title(f"track {track} -  {self.database.get_song_details(track).title}")
            plt.xlabel("offset (database time - sample time)")
            plt.show(block=False)
            input("press enter to close plot...")
            plt.close()

            # plt.savefig(os.path.join("/Users/jem/Desktop/blues_54_charts/", f"track {track}")+".png")
            # plt.close()

        # graph of std devs above mean for all tracks
        plt.figure(figsize=(8, 6))
        # plt.title(f"track {track} -  {self.database.get_song_details(track).title}")
        plt.title("standard deviations above mean (ordered by hash matches)")
        bar_labels = list(map(str, sd_a_means.keys()))
        bar_values = sd_a_means.values()
        bar_colours = list(map(self.bar_colour, sd_a_means.keys()))
        plt.bar(bar_labels, bar_values, color=bar_colours)
        plt.show(block=False)
        input("press enter to close plot...")
        plt.close()

        # graph of tallest bar for all tracks
        plt.figure(figsize=(8, 6))
        # plt.title(f"track {track} -  {self.database.get_song_details(track).title}")
        plt.title("tallest bar (ordered by hash matches)")
        bar_labels = list(map(str, tallest_bars.keys()))
        bar_values = tallest_bars.values()
        bar_colours = list(map(self.bar_colour, tallest_bars.keys()))
        plt.bar(bar_labels, bar_values, color=bar_colours)
        plt.show(block=False)
        input("press enter to close plot...")
        plt.close()

        # graph of tallest bar for all tracks
        plt.figure(figsize=(8, 6))
        # plt.title(f"track {track} -  {self.database.get_song_details(track).title}")
        plt.title("compound metric (ordered by hash matches)")
        bar_labels = list(map(str, izzy_graph.keys()))
        bar_values = izzy_graph.values()
        bar_colours = list(map(self.bar_colour, izzy_graph.keys()))
        plt.bar(bar_labels, bar_values, color=bar_colours)
        plt.show(block=False)
        input("press enter to close plot...")
        plt.close()


    # calculate a score for how good the sample matches a given track in the db
    def calc_track_score(self, track):

        # generate histogram

        offsets = []

        all_xs = []
        all_ys = []

        for k in self.sample_time_per_track[track].keys():
            all_xs += self.database_time_per_track[track][k]
            all_ys += self.sample_time_per_track[track][k]

        hough = Hough(all_xs, all_ys)
        grad = hough.get_line_grad()
        multiplier = 1/grad

        for k in self.sample_time_per_track[track].keys():

            for s in range(len(self.database_time_per_track[track][k])):
                # self.database_time_per_track[track][k][s] /= self.multiplier
                self.database_time_per_track[track][k][s] /= multiplier

            for (d, s) in zip(self.database_time_per_track[track][k], self.sample_time_per_track[track][k]):
                offsets.append(d - s)

        counts, _ = np.histogram(offsets, bins=145)

        # track score

        mean = np.mean(counts)
        std_dev = np.std(counts)
        tallest_bar = np.max(counts)
        sd_a_mean = (tallest_bar - mean) / std_dev
        score = sd_a_mean * sd_a_mean * tallest_bar

        return score


    # looks through top track hash hits until a match is found
    def match_to_db_track(self):

        # start with track with most hash hits
        track_keys = sorted(self.song_hits.keys(), key=lambda k: self.song_hits[k], reverse=True)

        # calculate first 50 scores
        # track_scores = [*map(self.calc_track_score, track_keys[:50])]
        track_scores = [*map(self.calc_track_score, track_keys[:200])]

        # return best match from caclulated scores
        return track_keys[np.argmax(track_scores)]


    def original_filename(self, path):

        filename = os.path.basename(path)
        return "_".join(filename.split("_")[:2])+".wav"


    # highlight correct song
    def bar_colour(self, track_id):

        root_filename = self.original_filename(self.filename)
        db_filename = self.database.get_song_details(track_id).title

        return "#697046" if db_filename == root_filename else "#4D4670"


    # display or save hash hits graph
    def hits_graph(self, save_file_instead=False):

        if len(self.sample_time_per_track.keys()) == 0:
            print("no hash hits")
            exit()

        sorted_keys = sorted(self.song_hits.keys())
        bar_labels = list(map(str, sorted_keys))
        bar_values = [self.song_hits[x] for x in sorted_keys]
        bar_colours = list(map(self.bar_colour, sorted_keys))

        plt.figure(figsize=(8, 6))
        plt.bar(bar_labels, bar_values, color=bar_colours)

        # plt.bar([str(x) for x in self.song_hits.keys()], self.song_hits.values(), color="#4D4670")
        # print(self.song_hits)

        plt.title(f"hash matches for '{os.path.basename(self.filename)}' in database")
        plt.xlabel("track number")
        plt.ylabel("hash matches")

        if save_file_instead:
            save_path = "hash_hits_graphs/"

            if not os.path.exists(save_path):
                os.makedirs(save_path)

            plt.savefig(os.path.join("hash_hits_graphs/", self.original_filename(self.filename))+".png")
        else:
            plt.show(block=False)
            input("press enter to close plot...")
            plt.close()


    def visualise_search(self):

        if len(self.sample_time_per_track.keys()) == 0:
            print("no hash hits")
            exit()

        self.hits_graph()

        for key in self.sample_time_per_track.keys():

            if key != 29: continue

            offsets = []
            plt.subplots(figsize=(12, 6))

            song_title = self.database.get_song_details(key).title

            # if song_title != "disco_00039.wav": continue

            for k in self.sample_time_per_track[key].keys():

                plt.scatter(self.database_time_per_track[key][k], self.sample_time_per_track[key][k], c="k", marker="x") # add c="k" for black

                for (d, s) in zip(self.database_time_per_track[key][k], self.sample_time_per_track[key][k]):
                    offsets.append(d - s)

            plt.title(f"track {key} ({song_title}) hash matches")
            plt.xlabel("database soundfile time")
            plt.ylabel("sample soundfile time")

            plt.show(block=False)
            input("press enter to close plot...")
            plt.close()


            counts, bins = np.histogram(offsets, bins=100)
            plt.stairs(counts, bins, color="#4D4670", fill=True)

            plt.title(f"track {key} ")
            plt.xlabel("offset (database time - sample time)")

            plt.show(block=False)
            input("press enter to close plot...")
            plt.close()