import pickle
from pathlib import Path
from collections import Counter
from utils import input_mp3, audio_to_spectrogram, spectrogram_to_peaks, peaks_to_fingerprints
from hashlib import md5

root = Path(".")
database_path = root / "database.txt"

def load_database(path):
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
    if not path.exists():
        err_msg = "The database path does not exist"
        raise AssertionError(err_msg)
    
    with open(path, mode="rb") as f:
        db = pickle.load(f)
    return db

def store_database(path, db):
    """ Stores a database (dictionary) as a pickled file

        Parameters
        ----------
        path: pathlib.Path 
            The path to the location where the database is to be stored
        
        db: Database
            The database to be stored

    """
    
    with open(path, mode="wb") as f:
        pickle.dump(db, f)

class database:
    def __init__(self):
        self.fps = dict()
        self.song_info = list()

def add_mp3(path, songs):
    """ Adds a song from a path into the database
        
        Parameters
        ----------
        path: pathlib.Path 
            The path to the location where the song is
        
        db: dict
            The database to be stored
    """

    if not path.exists():
        err_msg = "The mp3 path" + str(path) + "does not exist"
        raise AssertionError(err_msg)

    # index the song
    id = len(songs.song_info)
    song_name = path.stem
    songs.song_info.append(song_name) # we'll make this fancy later

    # fingerprint mp3
    S = audio_to_spectrogram(input_mp3(path))
    rows, cols = spectrogram_to_peaks(S)
    fingerprints = peaks_to_fingerprints(rows,cols)

    for key, t_match in fingerprints:
        if key in songs.fps:
            songs.fps[key].append((id, t_match))
        else:
            songs.fps[key] = [(id, t_match)]
    
def match_song(audio, songs):
    S = audio_to_spectrogram(audio)
    rows, cols = spectrogram_to_peaks(S)
    audio_fps = peaks_to_fingerprints(rows,cols)
    C = Counter()
    for finger_print, t in audio_fps:
        if finger_print in songs.fps:
            print(finger_print)
            id, t_match = songs.fps[finger_print]
            t_diff = t_match - t
            C[(id, t_diff)] += 1
    print(C)
    most_common, _ = C.most_common(1)
    return songs.song_info[most_common]
