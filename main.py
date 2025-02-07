from audio import Audio
from spectrogram import Spectrogram, PointMarker
from fingerprinter import Fingerprinter
from hasher import Hash, Hasher
from database import SongDetails, SongDatabase
import pickle


time_range = (None, None)
freq_range = (0, 5000)

re_process_songs = False
save_database = False

if re_process_songs:

    database = SongDatabase()
    songs = ["The Clocktower Reel.wav", "22 Remix.wav", "SEE NO EVIL.wav"]

    for song in songs:

        print(f"analysing \"{song}\"...")

        # load the audio, spectrogram and fingerprinter
        audio = Audio(song, 1)
        spectrogram = Spectrogram(audio.audio_data, audio.sampling_freq)
        fingeprinter = Fingerprinter(spectrogram.spectrum, spectrogram.row_freqs, spectrogram.col_times)

        # find the spectral peaks and add their point markers to the graph
        spectral_peaks = fingeprinter.find_peaks(*freq_range, *time_range)

        # generate the hashes
        hasher = Hasher(spectral_peaks)
        hashes = hasher.generate_hashes(True, False)

        for pm in spectral_peaks:
            spectrogram.add_point_marker(pm)

        spectrogram.display()
        spectrogram.display(freq_range)
        spectrogram.display(freq_range, False)

        # store the song in the database
        song_details = SongDetails(song, "unknown", "unknown")
        database.add_song(song_details, hashes)

    print("done processing")

    if save_database:
        with open("song_database", "wb") as db_file:
            pickle.dump(database, db_file)

        print("database dumped")
    else:
        print("not dumping database")

else:
    with open("song_database", "rb") as db_file:
        database = pickle.load(db_file)

    print("database loaded")











import numpy as np
import matplotlib.pyplot as plt


audio = Audio("clock sample.wav", 1)
spectrogram = Spectrogram(audio.audio_data, audio.sampling_freq)
fingeprinter = Fingerprinter(spectrogram.spectrum, spectrogram.row_freqs, spectrogram.col_times)
spectral_peaks = fingeprinter.find_peaks(*freq_range, *time_range)
hasher = Hasher(spectral_peaks)
hashes = hasher.generate_hashes(True, True)

song_hits = {}
sample_time_per_track = {}
database_time_per_track = {}


def store_hit(anchor_no, track_index, sample_offset, database_offset):

    if track_index not in sample_time_per_track:
        sample_time_per_track[track_index] = {}
        database_time_per_track[track_index] = {}

    if anchor_no not in sample_time_per_track[track_index]:
        sample_time_per_track[track_index][anchor_no] = []
        database_time_per_track[track_index][anchor_no] = []

    sample_time_per_track[track_index][anchor_no].append(sample_offset)
    database_time_per_track[track_index][anchor_no].append(database_offset)

    if track_index not in song_hits:
        song_hits[track_index] = 0

    song_hits[track_index] += 1


for anchor_no, anchor_group in enumerate(hashes):

    for anon_hash in anchor_group:

        hits = database.search_hash(anon_hash)

        if hits == None:
            continue

        for hit in hits:
            track_index, database_offset = hit
            store_hit(anchor_no, track_index, anon_hash.anchor_time_abs, database_offset)


if len(sample_time_per_track.keys()) == 0:
    print("no hash hits")
    exit()


plt.bar([str(x) for x in song_hits.keys()], song_hits.values(), color="#4D4670")
print(song_hits)

plt.title("hash matches for sample in database")
plt.xlabel("track number")
plt.ylabel("hash matches")

plt.show(block=False)
input("press enter to close plot...")
plt.close()


for key in sample_time_per_track.keys():

    offsets = []
    plt.subplots(figsize=(12, 6))

    for k in sample_time_per_track[key].keys():

        plt.scatter(database_time_per_track[key][k], sample_time_per_track[key][k], marker="x") # add c="k" for black

        for (d, s) in zip(database_time_per_track[key][k], sample_time_per_track[key][k]):
            offsets.append(d - s)

    plt.title(f"track {key} hash matches")
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