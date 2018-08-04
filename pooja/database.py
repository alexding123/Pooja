import pickle
from pathlib import Path
from collections import Counter
from .utils import input_mp3, audio_to_spectrogram, spectrogram_to_peaks, peaks_to_fingerprints, to_path_if_not_already
from hashlib import md5

root = Path(".")
database_path = root / "data"

class database:
    def __init__(self, path=None):
        self.fps = dict()
        self.song_info = list()
        if not path is None:
            self.load(path)

    def load(self, path):
        """ Loads a pickled dictionary that acts as the fingerprint databse

            Parameters
            ----------
            path: pathlib.Path 
                The path to the file to be read from

            Returns
            -------
            Database
                The database containing song info and fingerprints
        """
        path = to_path_if_not_already(path)
        if not path.exists():
            err_msg = "The database path does not exist"
            raise AssertionError(err_msg)
        
        with open(path, mode="rb") as f:
            db = pickle.load(f)
            self.fps = db.fps
            self.song_info = db.song_info
        

    def store(self, path):
        """ Stores a database (dictionary) as a pickled file

            Parameters
            ----------
            path: pathlib.Path 
                The path to the location where the database is to be stored
            
            db: Database
                The database to be stored

        """
        path = to_path_if_not_already(path)
        with open(path, mode="wb") as f:
            pickle.dump(self, f)
            
    def add_mp3(self, path):
        """ Adds a song from a path into the database
            
            Parameters
            ----------
            path: pathlib.Path 
                The path to the location where the song is
            
            db: dict
                The database to be stored
        """
        path = to_path_if_not_already(path)
        if not path.exists():
            err_msg = "The mp3 path" + str(path) + "does not exist"
            raise AssertionError(err_msg)

        # index the song
        id = len(self.song_info)
        song_name = path.stem
        self.song_info.append(song_name) # we'll make this fancy later

        # fingerprint mp3
        S = audio_to_spectrogram(input_mp3(path))
        freqs, times = spectrogram_to_peaks(S)
        fingerprints = peaks_to_fingerprints(freqs, times)

        for key, t_match in fingerprints:
            if key in self.fps:
                self.fps[key].append((id, t_match))
            else:
                self.fps[key] = [(id, t_match)]
                
    def match_song(self, audio):
        """Gets an audio file and turns compares it
            Parameters:
            ----------
            audio: the audio file that is to be compared to the self as a np.array

            Returns:
            -------
            Returns a string depending on what is the most common song. If the threshold is not met, it says no song is founds
        """
        length = round(len(audio) / 44100)
        S = audio_to_spectrogram(audio)
        freqs, times = spectrogram_to_peaks(S)
        audio_fps = peaks_to_fingerprints(freqs,times)
        C = Counter()
        for finger_print, t in audio_fps:
            if finger_print in self.fps:
                l = self.fps[finger_print]
                for id, t_match in l:
                    t_diff = t_match - t
                    C[(id, t_diff)] += 1
        if len(C.most_common()) == 0:
            return "No song found"
        fp_count = C.most_common(1)[0][1]
        if fp_count < length * 9:
            return self.song_info[C.most_common(1)[0][0][0]]
        else:
            return None

