import pickle
from pathlib import Path
from collections import Counter
from utils import input_mp3, audio_to_spectrogram, spectrogram_to_peaks, peaks_to_fingerprints
import hashlib

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
        dict((fn,fm,tm-tn)->list[(song_ID, tmatch)])
    """
    if not path.exists():
        err_msg = "The database path does not exist"
        raise AssertionError(err_msg)
    
    with open(path, mode="rb") as f:
        db, song_info = pickle.load(f)
    return db, song_info

def store_database(path, db, song_info):
    """ Stores a database (dictionary) as a pickled file

        Parameters
        ----------
        path: pathlib.Path 
            The path to the location where the database is to be stored
        
        db: dict
            The database to be stored

        Returns
        -------
        dict((fn,fm,tm-tn)->list[(song_ID, tmatch)])
    """
    if not path.exists():
        err_msg = "The database path does not exist"
        raise AssertionError(err_msg)
    
    with open(path, mode="wb") as f:
        pickle.dump((db, song_info), f)

class database:
    def __init__(self):
        self.fps = dict()
        self.song_info = dict()

def add_mp3(path, db):
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

    # find song's md5
    md5 = hashlib.md5(path).hexdigest()
    song_name = path.stem
    db.song_info[md5] = song_name # we'll make this fancy later

    # fingerprint mp3
    S = audio_to_spectrogram(input_mp3(path))
    rows, cols = spectrogram_to_peaks(S)
    fingerprints = peaks_to_fingerprints(rows,cols)
    for key, t_match in fingerprints:
        if key in db.fps:
            db.fps[key].append((md5, t_match))
        else:
            db.fps[key] = [(md5, t_match)]
    
def match_song(audio, db, song_info):
    S = audio_to_spectrogram(audio)
    rows, cols = spectrogram_to_peaks(S)
    audio_fps = peaks_to_fingerprints(rows, cols)
    C = Counter()
    for finger_print, t in (audio_fps):
        if finger_print in db:
            md5, t_match = db[finger_print]
            t_diff = t_match - t
            C[(md5, t_diff)] += 1
    most_common, _ = C.most_common(1)
    return song_info[most_common]
