import wave
import numpy as np


class Audio():

    def __init__(self, filename, channel=1):
        self.filename = filename
        self.channel_selection = channel

        self.channels_in_file = 0 # set by load
        self.audio_data = 0 # ndarray set by load
        self.sampling_freq = 0 # set by load
        self.load()

        self.prune_channels()
        

    # loads audio data from file into an ndarray
    def load(self):
        with wave.open(self.filename, "rb") as sound_file:
            assert sound_file.getsampwidth() == 2, "only 16 bit audio supported"

            self.channels_in_file = sound_file.getnchannels()
            self.sampling_freq = sound_file.getframerate()

            raw_data = sound_file.readframes(-1) # read all frames as bytes

        self.audio_data = np.frombuffer(raw_data, dtype=np.int16)


    # selects one audio channel (must be run after load)
    def prune_channels(self):
        assert 0 < self.channel_selection <= self.channels_in_file, "incorrect channel selection"

        if self.channels_in_file == 1: return # avoid unnecessary computation

        # start at channel selection skipping over other channels
        self.audio_data = self.audio_data[self.channel_selection-1::self.channels_in_file]