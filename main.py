from sample import Sample
import pickle, os


time_range = (None, None)
freq_range = (0, 5000)


# load database

print("loading database...")
with open("song_database", "rb") as db_file:
# with open("song_database_full", "rb") as db_file:
    database = pickle.load(db_file)
print("loaded")


# analyse sample

# sample_filename = "../small_qbe_dataset/samples/unchanged/blues_00000_o1.4624604095380658.wav"
# recorded_filename = "../small_qbe_dataset/recordings/unchanged/blues_00000_o1.4624604095380658_recorded.wav"

# sample = Sample(sample_filename, database, False)
# sample.load_stage_1()
# print("loaded sample")

# recorded = Sample(recorded_filename, database, False)
# recorded.load_stage_1()
# print("loaded recording")

# sample.show_peaks()
# recorded.show_peaks()


# save all hash hit graphs

# dataset_path = "../small_qbe_dataset/recordings/unchanged/"

# for filename in os.listdir(dataset_path):

#     if not filename.endswith(".wav"):
#         continue

#     print(f"testing '{filename}'...")

#     full_path = os.path.join(dataset_path, filename)

#     sample = Sample(full_path, database)
#     sample.hits_graph(save_file_instead=True)

#     print(f"saved '{filename}' hash hits graph")



# path = "../small_qbe_dataset/recordings/unchanged/blues_00054_o13.338763464108158_recorded.wav"
# path = "../small_qbe_dataset/recordings/unchanged/disco_00040_o18.993340807328412_recorded.wav"
# path = "../small_qbe_dataset/recordings/unchanged/reggae_00063_o5.6526555675347705_recorded.wav"
# path = "../small_qbe_dataset/recordings/unchanged/classical_00077_o1.529393028761099_recorded.wav"

# sample = Sample(path, database)
# # sample.original_filename(filename)

# sample.hits_graph()
# sample.match_to_db_track_old()




def get_multiplier(filename):

    parts = filename.split("_")

    for part in parts:
        if part[0] in ['t', 'x']:
            return float(part[1:])
    
    return 1

# dataset_path = "../small_qbe_dataset/recordings/unchanged/"
# dataset_path = "../small_qbe_dataset/recordings/unchanged_cafe/"
# dataset_path = "../small_qbe_dataset/recordings/unchanged_street/"

# dataset_path = "../small_qbe_dataset/recordings/pitch_altered/"
# dataset_path = "../small_qbe_dataset/recordings/pitch_and_tempo_altered/"
dataset_path = "../small_qbe_dataset/recordings/tempo_altered/"
# dataset_path = "../small_qbe_dataset/recordings/speed_altered/"

# dataset_paths = ["../small_qbe_dataset/recordings/unchanged/", "../small_qbe_dataset/recordings/unchanged_cafe/", "../small_qbe_dataset/recordings/unchanged_street/", "../small_qbe_dataset/recordings/pitch_altered/", "../small_qbe_dataset/recordings/pitch_and_tempo_altered/", "../small_qbe_dataset/recordings/tempo_altered/", "../small_qbe_dataset/recordings/speed_altered/"]

# for dataset_path in dataset_paths:

correct = 0
total = 0

for filename in os.listdir(dataset_path):

    if not filename.endswith(".wav"):
        continue

    # print(f"testing '{filename}'...")

    full_path = os.path.join(dataset_path, filename)

    m = get_multiplier(filename)
    sample = Sample(full_path, database, m)
    sample_name = sample.original_filename(filename)

    # if filename == "country_00025_t1.9295610185897236_o5.466721323818901_recorded.wav":
    #     # sample.hits_graph()
    #     sample.match_to_db_track_old()

    track_match = sample.match_to_db_track()
    title = database.get_song_details(track_match).title

    # print(f"matched {title}")

    print(sample_name, end=",")

    if sample_name == title:
        # print("correct")
        print("1")
        correct += 1
    else:
        # print("WRONG")
        print("0")

    total += 1

print("-------------------------")

print(dataset_path)
print(f"{correct} / {total} - {100 * correct/total} %")

print("-------------------------\n")