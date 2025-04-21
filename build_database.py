from audio import Audio
from spectrogram import Spectrogram, PointMarker
from fingerprinter import Fingerprinter
from hasher import Hash, Hasher
from database import SongDetails, SongDatabase

import pickle, os


time_range = (None, None)
freq_range = (0, 5000)

re_process_songs = True
save_database = True
show_graphs_while_processing = False

dataset_dir = "../small_qbe_dataset/full_songs/songs/"
# dataset_dir = "../small_qbe_dataset/all_songs/"
skip_songs = ["jazz_00054.wav"]


if re_process_songs:

    database = SongDatabase()

    for filename in os.listdir(dataset_dir):

        if not filename.endswith(".wav") or filename in skip_songs:
            continue

        song = os.path.join(dataset_dir, filename)

        print(f"analysing \"{song}\"...")

        # load the audio, spectrogram and fingerprinter
        audio = Audio(song)
        spectrogram = Spectrogram(audio.audio_data, audio.sampling_freq)
        fingeprinter = Fingerprinter(spectrogram.spectrum, spectrogram.row_freqs, spectrogram.col_times)

        # find the spectral peaks and add their point markers to the graph
        spectral_peaks = fingeprinter.find_peaks(*freq_range, *time_range)

        # generate the hashes
        hasher = Hasher(spectral_peaks)
        hashes = hasher.generate_hashes(True, False)

        for pm in spectral_peaks:
            spectrogram.add_point_marker(pm)

        if show_graphs_while_processing:
            spectrogram.display()
            spectrogram.display(freq_range)
            spectrogram.display(freq_range, False)

        # store the song in the database
        song_details = SongDetails(filename, "unknown", "unknown")
        database.add_song(song_details, hashes)

    print("done processing")

    if save_database:
        with open("song_database", "wb") as db_file:
            pickle.dump(database, db_file, protocol=pickle.HIGHEST_PROTOCOL)

        print("database dumped")
    else:
        print("not dumping database")