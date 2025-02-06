
class SongDetails():

    def __init__(self, title, album, artist):
        self.title = title
        self.album = album
        self.artist = artist


class SongHash():

    def __init__(self, anon_hash, track_index):
        self.anon_hash = anon_hash
        self.track_index = track_index
    
    def __hash__(self):
        return hash(self.anon_hash)


class SongDatabase():

    def __init__(self):
        self.songs = []
        self.song_hashes = {}


    def add_song(self, song_details, anon_song_hashes):

        next_song_index = len(self.songs)
        self.songs.append(song_details)

        for anon_song_hash in anon_song_hashes:
            song_hash = SongHash(anon_song_hash, next_song_index)

            h = hash(song_hash)
            if h in self.song_hashes:
                self.song_hashes[h].append(song_hash)
            else:
                self.song_hashes[h] = [song_hash]


    def search_hash(self, anon_hash):

        if hash(anon_hash) not in self.song_hashes:
            return None

        hits = self.song_hashes[hash(anon_hash)]

        return [(hit.track_index, hit.anon_hash.anchor_time_abs) for hit in hits]


    def get_song_details(self, song_index):

        return self.songs[song_index]


    def get_song_name(self, song_index):

        return self.get_song_details(song_index).title