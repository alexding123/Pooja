import pickle
from pathlib import Path
from utils import input_mp3, audio_to_spectrogram, spectrogram_to_peaks, peaks_to_fingerprints
import hashlib

root = Path(".")
database_path = root / "database.txt"
print(database_path)

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

def database():
    """ A fake constructor function that returns our database
        
        Returns
        -------
        dict((fn,fm,tm-tn)->list[(song_ID, tmatch)])
    """
    return dict()

def add_mp3(path, db, song_info):
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

    md5 = hashlib.md5(path).hexdigest()
    song_name = path.stem
    song_info[md5] = song_name # we'll make this fancy later
    S = audio_to_spectrogram(input_mp3(path))
    rows, cols = spectrogram_to_peaks(S)
    fingerprints = peaks_to_fingerprints(rows,cols)
    for key, t_match in fingerprints:
        db[key] = (md5, t_match)
    


